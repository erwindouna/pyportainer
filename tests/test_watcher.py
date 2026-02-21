"""Tests for the ImageWatcher background task."""
# pylint: disable=protected-access

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

import pytest
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from pyportainer.watcher import PortainerImageWatcher, PortainerImageWatcherResult
from tests import load_fixtures

if TYPE_CHECKING:
    from pyportainer import Portainer

IMAGE = "docker.io/library/ubuntu:latest"
CONTAINER_ID = "aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf"


async def test_image_watcher_check_all(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    snapshot: SnapshotAssertion,
) -> None:
    """Test that _check_all populates results with the update status per image."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("containers.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    await watcher._check_all()

    assert watcher.results == snapshot


async def test_image_watcher_results_copy(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    snapshot: SnapshotAssertion,
) -> None:
    """Test that results returns a copy so mutations don't affect the watcher state."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("containers.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    await watcher._check_all()

    results = watcher.results
    results.clear()
    assert watcher.results == snapshot


async def test_image_watcher_start_stop(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    snapshot: SnapshotAssertion,
) -> None:
    """Test that start() launches the task and stop() cancels it."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("containers.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    assert watcher._task is None

    watcher.start()
    assert watcher._task is not None
    assert not watcher._task.done()

    await asyncio.sleep(0.05)
    assert watcher.results == snapshot

    watcher.stop()
    await asyncio.sleep(0)
    assert watcher._task.done()


async def test_image_watcher_start_idempotent(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that calling start() twice reuses the same task."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("containers.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    watcher.start()
    task_first = watcher._task
    watcher.start()
    assert watcher._task is task_first

    watcher.stop()
    await asyncio.sleep(0)


@pytest.mark.parametrize(
    "status_code",
    [401, 404, 500],
)
async def test_image_watcher_check_all_exceptions(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    status_code: int,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that per-image errors during _check_all are logged but don't stop the watcher."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("containers.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{IMAGE}/json",
        "GET",
        aresponses.Response(text="Error response", status=status_code),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    with caplog.at_level(logging.WARNING):
        await watcher._check_all()

    assert not watcher.results
    assert "Failed to check image" in caplog.text


def _add_image_check_responses(aresponses: ResponsesMockServer) -> None:
    """Add the standard three responses needed for a single image check."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("containers.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )


async def test_image_watcher_sync_callback(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that a synchronous callback is invoked for each result."""
    _add_image_check_responses(aresponses)

    received: list[PortainerImageWatcherResult] = []

    def my_callback(result: PortainerImageWatcherResult) -> None:
        """Append result to the received list."""
        received.append(result)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    watcher.register_callback(my_callback)
    await watcher._check_all()

    assert len(received) == len(watcher.results)
    assert all(r in watcher.results.values() for r in received)


async def test_image_watcher_async_callback(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that an async callback is awaited for each result."""
    _add_image_check_responses(aresponses)

    received: list[PortainerImageWatcherResult] = []

    async def my_async_callback(result: PortainerImageWatcherResult) -> None:
        """Append result to the received list."""
        received.append(result)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    watcher.register_callback(my_async_callback)
    await watcher._check_all()

    assert len(received) == len(watcher.results)


async def test_image_watcher_callback_duplicate_ignored(
    portainer_client: Portainer,
) -> None:
    """Test that registering the same callback twice only calls it once per result."""

    def my_callback(result: PortainerImageWatcherResult) -> None:  # pylint: disable=unused-argument
        """Do nothing; used to test duplicate registration handling."""

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    watcher.register_callback(my_callback)
    watcher.register_callback(my_callback)

    assert watcher._callbacks.count(my_callback) == 1


async def test_image_watcher_unregister_callback(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that an unregistered callback is no longer called."""
    _add_image_check_responses(aresponses)

    received: list[PortainerImageWatcherResult] = []

    def my_callback(result: PortainerImageWatcherResult) -> None:
        """Append result to the received list."""
        received.append(result)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    watcher.register_callback(my_callback)
    watcher.unregister_callback(my_callback)
    await watcher._check_all()

    assert received is None or len(received) == 0


async def test_image_watcher_callback_exception_logged(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that a callback exception is logged but does not stop the watcher."""
    _add_image_check_responses(aresponses)

    def bad_callback(result: PortainerImageWatcherResult) -> None:  # noqa: ARG001  # pylint: disable=unused-argument
        """Raise an exception to test error handling."""
        msg = "boom"
        raise RuntimeError(msg)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    watcher.register_callback(bad_callback)

    with caplog.at_level(logging.ERROR):
        await watcher._check_all()

    assert watcher.results  # Results still populated despite callback failure
    assert "Callback raised an exception" in caplog.text
