"""Tests for the ImageWatcher background task."""
# pylint: disable=protected-access

from __future__ import annotations

import asyncio
import json
import logging
from typing import TYPE_CHECKING

import pytest
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from pyportainer.watcher import PortainerImageWatcher, PortainerImageWatcherResult
from tests import load_fixtures

if TYPE_CHECKING:
    from collections.abc import Generator

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


@pytest.fixture(name="preserve_watcher_log_level")
def _preserve_watcher_log_level() -> Generator[None, None, None]:
    """Restore the watcher logger's level after a test changes it."""
    logger = logging.getLogger("pyportainer.watcher")
    original = logger.level
    yield
    logger.setLevel(original)


@pytest.mark.usefixtures("preserve_watcher_log_level")
@pytest.mark.parametrize(
    ("debug", "expected"),
    [(False, logging.ERROR), (True, logging.DEBUG)],
)
def test_watcher_never_lowers_the_configured_log_level(
    portainer_client: Portainer,
    *,
    debug: bool,
    expected: int,
) -> None:
    """Test that constructing a watcher doesn't undo the application's logger configuration."""
    logger = logging.getLogger("pyportainer.watcher")
    logger.setLevel(logging.ERROR)

    PortainerImageWatcher(portainer_client, endpoint_id=1, debug=debug)

    assert logger.level == expected


MOVED_TAG_CONTAINER_ID = "1111111111111111111111111111111111111111111111111111111111111111"
MOVED_TAG_IMAGE_ID = "sha256:2222222222222222222222222222222222222222222222222222222222222222"
MOVED_TAG_IMAGE = "portainer/portainer-ce:latest"
STOPPED_CONTAINER_ID = "3333333333333333333333333333333333333333333333333333333333333333"
SECOND_CONTAINER_ID = "4444444444444444444444444444444444444444444444444444444444444444"
OLD_DIGEST = "sha256:5555555555555555555555555555555555555555555555555555555555555555"
REGISTRY_DIGEST = "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96"


def _add_container_list(aresponses: ResponsesMockServer, image: str) -> None:
    """Add a container list with a running and a stopped container listed by image ID."""
    containers = [
        {"Id": MOVED_TAG_CONTAINER_ID, "Image": image, "State": "running"},
        {"Id": STOPPED_CONTAINER_ID, "Image": image, "State": "exited"},
    ]
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=json.dumps(containers),
        ),
    )


def _add_container_inspect(
    aresponses: ResponsesMockServer,
    config_image: str | None,
    container_id: str = MOVED_TAG_CONTAINER_ID,
) -> None:
    """Add an inspect response with the given Config.Image."""
    inspect = {"Id": container_id, "Image": MOVED_TAG_IMAGE_ID, "Config": {"Image": config_image}}
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/containers/{container_id}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=json.dumps(inspect),
        ),
    )


@pytest.mark.parametrize(
    "listed_image",
    [
        pytest.param(MOVED_TAG_IMAGE_ID, id="sha256_prefix"),
        pytest.param(MOVED_TAG_IMAGE_ID.removeprefix("sha256:"), id="bare_hex"),
    ],
)
@pytest.mark.parametrize(
    ("local_digest", "update_available"),
    [
        pytest.param(OLD_DIGEST, True, id="old_image"),
        pytest.param(REGISTRY_DIGEST, False, id="up_to_date"),
    ],
)
async def test_image_watcher_resolves_image_id(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    listed_image: str,
    local_digest: str,
    *,
    update_available: bool,
) -> None:
    """Test that containers listed by image ID compare the image they run with the registry."""
    containers = [
        {"Id": MOVED_TAG_CONTAINER_ID, "Image": listed_image, "State": "running"},
        {"Id": SECOND_CONTAINER_ID, "Image": listed_image, "State": "running"},
    ]
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=json.dumps(containers),
        ),
    )
    _add_container_inspect(aresponses, MOVED_TAG_IMAGE)
    _add_container_inspect(aresponses, MOVED_TAG_IMAGE, SECOND_CONTAINER_ID)
    # One registry and one local lookup shared by both containers on the same image.
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/distribution/{MOVED_TAG_IMAGE}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/images/{listed_image}/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=json.dumps({"Id": MOVED_TAG_IMAGE_ID, "RepoDigests": [f"portainer/portainer-ce@{local_digest}"]}),
        ),
    )

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    await watcher._check_all()

    assert set(watcher.results) == {(1, MOVED_TAG_CONTAINER_ID), (1, SECOND_CONTAINER_ID)}
    for result in watcher.results.values():
        assert result.status is not None
        assert result.status.update_available is update_available
        assert result.status.local_digest == local_digest
        assert result.status.registry_digest == REGISTRY_DIGEST
    aresponses.assert_no_unused_routes()
    aresponses.assert_all_requests_matched()


@pytest.mark.parametrize(
    "config_image",
    [
        pytest.param(MOVED_TAG_IMAGE_ID, id="sha256_prefix"),
        pytest.param(MOVED_TAG_IMAGE_ID.removeprefix("sha256:"), id="bare_hex"),
        pytest.param(None, id="missing"),
    ],
)
async def test_image_watcher_skips_container_without_reference(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    caplog: pytest.LogCaptureFixture,
    config_image: str | None,
) -> None:
    """Test that a container created from an image ID is skipped without a registry lookup."""
    _add_container_list(aresponses, MOVED_TAG_IMAGE_ID)
    _add_container_inspect(aresponses, config_image)

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    with caplog.at_level(logging.DEBUG, logger="pyportainer.watcher"):
        await watcher._check_all()

    assert not watcher.results
    assert "has no registry reference" in caplog.text
    assert not [record for record in caplog.records if record.levelno >= logging.WARNING]
    aresponses.assert_no_unused_routes()
    aresponses.assert_all_requests_matched()


async def test_image_watcher_skips_container_on_inspect_error(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that a failed inspect skips only that container."""
    _add_container_list(aresponses, MOVED_TAG_IMAGE_ID)
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/1/docker/containers/{MOVED_TAG_CONTAINER_ID}/json",
        "GET",
        aresponses.Response(text="Not found", status=404),
    )

    watcher = PortainerImageWatcher(portainer_client, endpoint_id=1)
    with caplog.at_level(logging.DEBUG, logger="pyportainer.watcher"):
        await watcher._check_all()

    assert not watcher.results
    assert "Failed to inspect container" in caplog.text
    assert not [record for record in caplog.records if record.levelno >= logging.WARNING]
    aresponses.assert_no_unused_routes()
    aresponses.assert_all_requests_matched()
