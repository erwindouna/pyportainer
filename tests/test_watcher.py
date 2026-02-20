"""Tests for the ImageWatcher background task."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from aresponses import ResponsesMockServer

from pyportainer.watcher import PortainerImageWatcher
from tests import load_fixtures

if TYPE_CHECKING:
    from pyportainer import Portainer

IMAGE = "docker.io/library/ubuntu:latest"


def _add_containers_response(aresponses: ResponsesMockServer) -> None:
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


def _add_image_check_responses(aresponses: ResponsesMockServer, image: str) -> None:
    """Register mocked responses for a single has_new_image() call."""
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{image}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{image}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )


async def test_image_watcher_check_all(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that _check_all populates results with the update status per image."""
    _add_containers_response(aresponses)
    _add_image_check_responses(aresponses, IMAGE)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    await watcher._check_all()

    assert IMAGE in watcher.results
    assert watcher.results[IMAGE].update_available is True
    assert watcher.results[IMAGE].registry_digest == ("sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96")


async def test_image_watcher_results_copy(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that results returns a copy so mutations don't affect the watcher state."""
    _add_containers_response(aresponses)
    _add_image_check_responses(aresponses, IMAGE)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    await watcher._check_all()

    snapshot = watcher.results
    snapshot.clear()
    assert IMAGE in watcher.results  # original state unaffected


async def test_image_watcher_start_stop(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that start() launches the task and stop() cancels it."""
    _add_containers_response(aresponses)
    _add_image_check_responses(aresponses, IMAGE)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    assert watcher._task is None

    watcher.start()
    assert watcher._task is not None
    assert not watcher._task.done()

    # Let the first check run and settle into the interval sleep
    await asyncio.sleep(0.05)

    assert IMAGE in watcher.results

    watcher.stop()
    # Give the cancellation a chance to propagate
    await asyncio.sleep(0)
    assert watcher._task.done()


async def test_image_watcher_start_idempotent(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that calling start() twice reuses the same task."""
    _add_containers_response(aresponses)
    _add_image_check_responses(aresponses, IMAGE)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    watcher.start()
    task_first = watcher._task
    watcher.start()  # second call — should be a no-op
    assert watcher._task is task_first

    watcher.stop()
    await asyncio.sleep(0)
