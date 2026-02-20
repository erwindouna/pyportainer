"""Background image update watcher."""

from __future__ import annotations

import asyncio
import logging
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING

from pyportainer.exceptions import PortainerAuthenticationError, PortainerConnectionError, PortainerError, PortainerTimeoutError

if TYPE_CHECKING:
    from pyportainer.models.docker import PortainerImageUpdateStatus
    from pyportainer.pyportainer import Portainer


_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class PortainerImageWatcherResult:
    """Represents the status of an image watcher."""

    endpoint_id: int | None = None
    container_id: str | None = None
    status: PortainerImageUpdateStatus | None = None


class PortainerImageWatcher:
    """Periodically checks all containers on an endpoint for image updates.

    Results are stored and accessible via the `results` property after each check.
    """

    def __init__(
        self,
        portainer: Portainer,
        endpoint_id: int | None = None,
        interval: timedelta = timedelta(hours=12),
        *,
        debug: bool = False,
    ) -> None:
        """Initialize the PortainerImageWatcher.

        Args:
        ----
            portainer: An authenticated Portainer client instance.
            endpoint_id: The ID of the endpoint whose containers to monitor. If None, all endpoints are monitored.
            interval: How often to poll for updates. Defaults to 12 hours.

        """
        self._portainer = portainer
        self._endpoint_id = endpoint_id
        self._interval = interval
        self._results: list[PortainerImageWatcherResult] = []
        self._task: asyncio.Task[None] | None = None
        self._last_check: float | None = None

        _LOGGER.setLevel(logging.DEBUG if debug else logging.INFO)

    @property
    def interval(self) -> timedelta:
        """Polling interval."""
        return self._interval

    @interval.setter
    def interval(self, value: timedelta) -> None:
        """Update the polling interval. Takes effect after the next check."""
        self._interval = value

    @property
    def last_check(self) -> float | None:
        """Timestamp of the last completed check, or None if no checks have completed yet."""
        return self._last_check

    @property
    def results(self) -> list[PortainerImageWatcherResult]:
        """Latest update status as of the last check."""
        return self._results

    def start(self) -> None:
        """Start the background polling loop.

        The first check runs immediately; subsequent checks run after each interval.
        Must be called from within a running asyncio event loop.
        """
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._run())

    def stop(self) -> None:
        """Cancel the background polling loop."""
        if self._task and not self._task.done():
            self._task.cancel()

    async def _run(self) -> None:
        """Loop that checks immediately, then sleep for the interval, then repeat.

        Errors during checks are logged but don't stop the watcher, allowing
        recovery from transient issues.
        """
        while True:
            try:
                await self._check_all()
                self._last_check = time.time()
            except PortainerTimeoutError:
                _LOGGER.exception("Timeout during image check")
            except PortainerConnectionError:
                _LOGGER.exception("Connection error during image check")
            except PortainerAuthenticationError:
                _LOGGER.exception("Authentication error during image check")
            except PortainerError:
                _LOGGER.exception("Error during image check")

            await asyncio.sleep(self._interval.total_seconds())

    async def _check_all(self) -> None:
        """Fetch all containers and check each unique image concurrently.

        Errors for individual images are logged but silently skipped so one
        failing image does not prevent the rest from being checked.
        """
        if self._endpoint_id is not None:
            endpoint_ids: list[int] = [self._endpoint_id]
        else:
            _LOGGER.debug("No endpoint_id specified, fetching all endpoints to check.")
            endpoints = await self._portainer.get_endpoints()
            endpoint_ids = [endpoint.id for endpoint in endpoints]

        for endpoint_id in endpoint_ids:
            containers = await self._portainer.get_containers(endpoint_id)

            image_containers = defaultdict(list)
            for container in containers:
                if container.image and container.state == "running":
                    image_containers[container.image].append(container.id)

            _LOGGER.debug("Checking %d unique images for endpoint %s...", len(image_containers), endpoint_id)

            statuses = await asyncio.gather(
                *(self._portainer.container_image_status(endpoint_id, image) for image in image_containers),
                return_exceptions=True,
            )
            for image, status in zip(image_containers, statuses, strict=False):
                if isinstance(status, BaseException):
                    _LOGGER.warning("Failed to check image %s on endpoint %s: %s", image, endpoint_id, status)
                    continue
                for container_id in image_containers[image]:
                    self._results.append(
                        PortainerImageWatcherResult(
                            endpoint_id=endpoint_id,
                            container_id=container_id,
                            status=status,
                        )
                    )

                    _LOGGER.debug("Checked image %s on endpoint %s for container %s", image, endpoint_id, container_id)
