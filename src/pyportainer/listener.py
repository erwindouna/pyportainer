"""Background Docker event listener."""

from __future__ import annotations

import asyncio
import logging
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING

from pyportainer.exceptions import PortainerAuthenticationError, PortainerConnectionError, PortainerError, PortainerTimeoutError

if TYPE_CHECKING:
    from pyportainer.models.event import DockerEvent
    from pyportainer.pyportainer import Portainer


_LOGGER = logging.getLogger(__name__)

EventListenerCallback = Callable[["PortainerEventListenerResult"], Awaitable[None] | None]

#: Key used to track endpoint-discovery retries, which aren't tied to an endpoint ID.
_DISCOVERY_KEY = "__endpoint_discovery__"


@dataclass(frozen=True)
class PortainerEventListenerResult:
    """Represents a single Docker event received from an endpoint."""

    endpoint_id: int
    event: DockerEvent


class PortainerEventListener:
    """Maintains persistent streaming connections to Docker event endpoints.

    One streaming connection is opened per endpoint. Events are delivered to
    registered callbacks as they arrive, in real time. If a connection drops,
    it is automatically re-established after ``reconnect_interval``, with the
    delay doubling on each consecutive failure up to ``max_reconnect_interval``.
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-instance-attributes
        self,
        portainer: Portainer,
        endpoint_id: int | None = None,
        *,
        event_types: list[str] | None = None,
        reconnect_interval: timedelta = timedelta(seconds=5),
        max_reconnect_interval: timedelta = timedelta(minutes=5),
        debug: bool = False,
    ) -> None:
        """Initialize the PortainerEventListener.

        Args:
        ----
            portainer: An authenticated Portainer client instance.
            endpoint_id: The ID of the endpoint to listen to. If None, all
                endpoints are monitored concurrently.
            event_types: Docker event types to filter on, e.g.
                ``["container", "image"]``. If None, all event types are
                delivered.
            reconnect_interval: How long to wait before the first reconnect
                attempt after a dropped connection. Defaults to 5 seconds. The
                delay doubles on each consecutive failure.
            max_reconnect_interval: Upper bound on the reconnect delay.
                Defaults to 5 minutes.
            debug: Raise this logger's level to DEBUG. Logging is otherwise
                left entirely to the application; the level configured by the
                caller is never lowered or overwritten.

        """
        self._portainer = portainer
        self._endpoint_id = endpoint_id
        self._event_types = event_types
        self._reconnect_interval = reconnect_interval
        self._max_reconnect_interval = max_reconnect_interval
        self._task: asyncio.Task[None] | None = None
        self._callbacks: list[EventListenerCallback] = []
        self._failures: dict[int | str, int] = {}

        if debug:
            _LOGGER.setLevel(logging.DEBUG)

    def start(self) -> None:
        """Start listening for Docker events.

        Opens streaming connections immediately. Must be called from within a
        running asyncio event loop.
        """
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._run())

    def stop(self) -> None:
        """Stop all streaming connections."""
        if self._task and not self._task.done():
            self._task.cancel()

    def register_callback(self, callback: EventListenerCallback) -> None:
        """Register a callback to be invoked for every Docker event received.

        Both synchronous and async callables are supported. The callback
        receives a single :class:`PortainerEventListenerResult` argument.
        Each unique callable is only registered once; duplicates are ignored.

        Args:
        ----
            callback: A sync or async callable that accepts a
                :class:`PortainerEventListenerResult`.

        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unregister_callback(self, callback: EventListenerCallback) -> None:
        """Remove a previously registered callback.

        Args:
        ----
            callback: The callable to remove. Raises :exc:`ValueError` if it
                was not registered.

        """
        self._callbacks.remove(callback)

    async def _fire_callbacks(self, result: PortainerEventListenerResult) -> None:
        """Invoke all registered callbacks for a single event.

        Exceptions raised by individual callbacks are logged but do not stop
        the listener.
        """
        for callback in list(self._callbacks):
            try:
                ret = callback(result)
                if asyncio.iscoroutine(ret):
                    await ret
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    "Callback raised an exception for event %s on endpoint %s",
                    result.event.action,
                    result.endpoint_id,
                )

    async def _backoff(self, key: int | str, message: str, err: Exception, *, exc_info: bool = False) -> None:
        """Log a failed attempt and sleep out the reconnect delay.

        The delay doubles with each consecutive failure on ``key``, capped at
        ``max_reconnect_interval``, with a little jitter so several endpoints
        failing at once don't all retry in lockstep. Only the first failure of
        a streak is logged at warning level; the rest are logged at debug
        level so a persistently unreachable endpoint doesn't flood the log.

        Args:
        ----
            key: Endpoint ID, or :data:`_DISCOVERY_KEY` for endpoint discovery.
            message: What went wrong, e.g. ``"Timeout on endpoint 5"``.
            err: The exception that ended the attempt.
            exc_info: Whether to log a traceback with the first warning.

        """
        failures = self._failures.get(key, 0) + 1
        self._failures[key] = failures

        base = self._reconnect_interval.total_seconds()
        ceiling = max(base, self._max_reconnect_interval.total_seconds())
        delay = min(base * 2 ** (failures - 1), ceiling) * random.uniform(0.8, 1.0)  # noqa: S311 - jitter, not security

        verb = "retrying" if key == _DISCOVERY_KEY else "reconnecting"
        if failures == 1:
            _LOGGER.warning("%s, %s in %.1fs: %s", message, verb, delay, err, exc_info=exc_info)
        else:
            _LOGGER.debug("%s, %s in %.1fs (attempt %d): %s", message, verb, delay, failures, err)

        await asyncio.sleep(delay)

    def _reset_failures(self, key: int | str) -> None:
        """Clear a failure streak, e.g. after a successful reconnect."""
        if self._failures.pop(key, None):
            _LOGGER.info("Recovered on %s after previous failures", "endpoint discovery" if key == _DISCOVERY_KEY else f"endpoint {key}")

    async def _listen(self, endpoint_id: int) -> None:
        """Stream events from a single endpoint and fire callbacks for each.

        Args:
        ----
            endpoint_id: The endpoint to stream events from.

        """
        filters = {"type": self._event_types} if self._event_types else None
        async for event in self._portainer.get_events(endpoint_id, filters=filters):
            self._reset_failures(endpoint_id)
            result = PortainerEventListenerResult(endpoint_id=endpoint_id, event=event)
            await self._fire_callbacks(result)

    async def _listen_with_reconnect(self, endpoint_id: int) -> None:
        """Stream events from an endpoint, reconnecting on transient errors.

        Authentication errors are treated as fatal and stop the listener for
        that endpoint. All other :class:`~pyportainer.exceptions.PortainerError`
        subclasses trigger a reconnect after a backoff delay; see
        :meth:`_backoff` for the backoff and log-throttling policy.

        Args:
        ----
            endpoint_id: The endpoint to stream events from.

        """
        while True:
            try:
                await self._listen(endpoint_id)
            except PortainerAuthenticationError:
                _LOGGER.exception(
                    "Authentication error for endpoint %s, stopping listener",
                    endpoint_id,
                )
                return
            except PortainerTimeoutError as err:
                await self._backoff(endpoint_id, f"Timeout on endpoint {endpoint_id}", err)
            except PortainerConnectionError as err:
                await self._backoff(endpoint_id, f"Connection lost on endpoint {endpoint_id}", err)
            except PortainerError as err:
                await self._backoff(endpoint_id, f"Error on endpoint {endpoint_id}", err, exc_info=True)

    async def _resolve_endpoint_ids(self) -> list[int]:
        """Resolve the list of endpoint IDs to listen to.

        Returns
        -------
            The list of endpoint IDs to listen to.

        """
        if self._endpoint_id is not None:
            return [self._endpoint_id]

        _LOGGER.debug("No endpoint_id specified, fetching all endpoints to listen to.")
        while True:
            try:
                endpoints = await self._portainer.get_endpoints()
            except PortainerTimeoutError as err:
                await self._backoff(_DISCOVERY_KEY, "Timeout fetching endpoints", err)
            except PortainerConnectionError as err:
                await self._backoff(_DISCOVERY_KEY, "Connection error fetching endpoints", err)
            else:
                self._reset_failures(_DISCOVERY_KEY)
                return [endpoint.id for endpoint in endpoints]

    async def _run(self) -> None:
        """Resolve endpoints and open a streaming connection to each.

        Endpoint discovery (when no explicit ``endpoint_id`` was supplied)
        retries indefinitely on transient errors; see
        :meth:`_resolve_endpoint_ids`.

        """
        endpoint_ids = await self._resolve_endpoint_ids()

        results = await asyncio.gather(
            *(self._listen_with_reconnect(ep_id) for ep_id in endpoint_ids),
            return_exceptions=True,
        )

        for endpoint_id, result in zip(endpoint_ids, results, strict=True):
            if isinstance(result, BaseException):
                _LOGGER.error(
                    "Listener for endpoint %s terminated unexpectedly",
                    endpoint_id,
                    exc_info=result,
                )
