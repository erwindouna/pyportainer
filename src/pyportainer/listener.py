"""Background Docker event listener."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING

from pyportainer.exceptions import PortainerAuthenticationError, PortainerConnectionError, PortainerError, PortainerTimeoutError

if TYPE_CHECKING:
    from pyportainer.models.docker import DockerEvent
    from pyportainer.pyportainer import Portainer


_LOGGER = logging.getLogger(__name__)

EventListenerCallback = Callable[["PortainerEventListenerResult"], Awaitable[None] | None]


@dataclass(frozen=True)
class PortainerEventListenerResult:
    """Represents a single Docker event received from an endpoint."""

    endpoint_id: int
    event: DockerEvent


class PortainerEventListener:
    """Maintains persistent streaming connections to Docker event endpoints.

    One streaming connection is opened per endpoint. Events are delivered to
    registered callbacks as they arrive, in real time. If a connection drops,
    it is automatically re-established after ``reconnect_interval``.
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-instance-attributes
        self,
        portainer: Portainer,
        endpoint_id: int | None = None,
        *,
        event_types: list[str] | None = None,
        reconnect_interval: timedelta = timedelta(seconds=5),
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
            reconnect_interval: How long to wait before reconnecting after a
                dropped connection. Defaults to 5 seconds.
            debug: Enable debug logging.

        """
        self._portainer = portainer
        self._endpoint_id = endpoint_id
        self._event_types = event_types
        self._reconnect_interval = reconnect_interval
        self._task: asyncio.Task[None] | None = None
        self._callbacks: list[EventListenerCallback] = []

        _LOGGER.setLevel(logging.DEBUG if debug else logging.INFO)

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

    async def _listen(self, endpoint_id: int) -> None:
        """Stream events from a single endpoint and fire callbacks for each.

        Args:
        ----
            endpoint_id: The endpoint to stream events from.

        """
        filters = {"type": self._event_types} if self._event_types else None
        async for event in self._portainer.get_events(endpoint_id, filters=filters):
            result = PortainerEventListenerResult(endpoint_id=endpoint_id, event=event)
            await self._fire_callbacks(result)

    async def _listen_with_reconnect(self, endpoint_id: int) -> None:
        """Stream events from an endpoint, reconnecting on transient errors.

        Authentication errors are treated as fatal and stop the listener for
        that endpoint. All other :class:`~pyportainer.exceptions.PortainerError`
        subclasses trigger a reconnect after ``reconnect_interval``.

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
            except PortainerTimeoutError:
                _LOGGER.warning(
                    "Timeout on endpoint %s, reconnecting in %ss",
                    endpoint_id,
                    self._reconnect_interval.total_seconds(),
                )
            except PortainerConnectionError:
                _LOGGER.warning(
                    "Connection lost on endpoint %s, reconnecting in %ss",
                    endpoint_id,
                    self._reconnect_interval.total_seconds(),
                )
            except PortainerError:
                _LOGGER.exception(
                    "Error on endpoint %s, reconnecting in %ss",
                    endpoint_id,
                    self._reconnect_interval.total_seconds(),
                )

            await asyncio.sleep(self._reconnect_interval.total_seconds())

    async def _run(self) -> None:
        """Resolve endpoints and open a streaming connection to each.

        Runs all per-endpoint listeners concurrently via :func:`asyncio.gather`.
        """
        if self._endpoint_id is not None:
            endpoint_ids: list[int] = [self._endpoint_id]
        else:
            _LOGGER.debug("No endpoint_id specified, fetching all endpoints to listen to.")
            endpoints = await self._portainer.get_endpoints()
            endpoint_ids = [endpoint.id for endpoint in endpoints]

        await asyncio.gather(*(self._listen_with_reconnect(ep_id) for ep_id in endpoint_ids))
