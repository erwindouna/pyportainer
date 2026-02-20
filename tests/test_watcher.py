"""Tests for the ImageWatcher background task."""
# pylint: disable=protected-access

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

import pytest
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from pyportainer.watcher import PortainerImageWatcher
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
