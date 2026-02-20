"""Background image update watcher."""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import timedelta
from typing import TYPE_CHECKING

from pyportainer.exceptions import (
    PortainerWatcherAuthenticationError,
    PortainerWatcherConnectionError,
    PortainerWatcherError,
    PortainerWatcherTimeoutError,
)
from pyportainer.models.docker import PortainerImageUpdateStatus

if TYPE_CHECKING:
    from pyportainer.pyportainer import Portainer

_LOGGER = logging.getLogger(__name__)


class PortainerImageWatcher:
    """Periodically checks all containers on an endpoint for image updates.

    Results are stored and accessible via the `results` property after each check.
    """

    def __init__(
        self,
        portainer: Portainer,
        endpoint_id: int | None = None,
        interval: timedelta = timedelta(hours=12),
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
        self._results: dict[str, PortainerImageUpdateStatus] = {}
        self._task: asyncio.Task[None] | None = None
        self._last_check: float | None = None

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
    def results(self) -> dict[str, PortainerImageUpdateStatus]:
        """Latest update status keyed by image name, as of the last check."""
        return dict(self._results)

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
        """Main loop: check immediately, then sleep for the interval, then repeat.

        Errors during checks are logged but don't stop the watcher, allowing
        recovery from transient issues.
        """
        while True:
            try:
                await self._check_all()
                self._last_check = time.time()
            except (
                PortainerWatcherConnectionError,
                PortainerWatcherAuthenticationError,
                PortainerWatcherTimeoutError,
                PortainerWatcherError,
            ) as err:
                _LOGGER.error("Error during image check: %s", err)
            except Exception as err:
                _LOGGER.exception("Unexpected error during image check: %s", err)

            await asyncio.sleep(self._interval.total_seconds())

    async def _check_all(self) -> None:
        """Fetch all containers and check each unique image concurrently.

        Errors for individual images are logged but silently skipped so one
        failing image does not prevent the rest from being checked.
        """
        endpoint_ids = [self._endpoint_id]
        if self._endpoint_id is None:
            endpoints = await self._portainer.get_endpoints()
            endpoint_ids = [endpoint.id for endpoint in endpoints]

        for endpoint_id in endpoint_ids:
            assert endpoint_id is not None
            containers = await self._portainer.get_containers(endpoint_id)
            unique_images = {container.image for container in containers if container.image}

            statuses = await asyncio.gather(
                *(self._portainer.container_image_status(endpoint_id, image) for image in unique_images),
                return_exceptions=True,
            )
            for image, status in zip(unique_images, statuses, strict=False):
                if isinstance(status, PortainerImageUpdateStatus):
                    self._results[image] = status
                elif isinstance(status, Exception):
                    _LOGGER.debug("Failed to check image %s: %s", image, status)
