"""Tests for the ImageWatcher background task."""
# pylint: disable=protected-access

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from pyportainer.exceptions import PortainerAuthenticationError, PortainerConnectionError, PortainerNotFoundError
from pyportainer.watcher import PortainerImageWatcher
from tests import load_fixtures

if TYPE_CHECKING:
    from pyportainer import Portainer

IMAGE = "docker.io/library/ubuntu:latest"


async def test_image_watcher_check_all(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
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

    assert IMAGE in watcher.results
    assert watcher.results[IMAGE].update_available is True
    assert watcher.results[IMAGE].registry_digest == ("sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96")


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
    ("status_code", "expected_exception"),
    [
        (401, PortainerAuthenticationError),
        (404, PortainerNotFoundError),
        (500, PortainerConnectionError),
    ],
)
async def test_image_watcher_check_all_exceptions(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    status_code: int,
    expected_exception: type[Exception],
) -> None:
    """Test that errors during _check_all are logged but don't stop the watcher."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("endpoints.json"),
        ),
    )
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

    watcher = PortainerImageWatcher(portainer_client)
    with pytest.raises(expected_exception):
        await watcher._check_all()

    assert not watcher.results
