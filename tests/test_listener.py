"""Tests for the PortainerEventListener background task."""
# pylint: disable=protected-access

from __future__ import annotations

import asyncio
import contextlib
import logging
from datetime import timedelta
from typing import TYPE_CHECKING

import pytest
from aiohttp.web import Request, Response
from aresponses import ResponsesMockServer

from pyportainer.exceptions import PortainerError
from pyportainer.listener import PortainerEventListener, PortainerEventListenerResult
from tests import load_fixtures

if TYPE_CHECKING:
    from pyportainer import Portainer

ENDPOINT_ID = 1
CONTAINER_ID = "aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf"


def _events_response(aresponses: ResponsesMockServer, *, status: int = 200, body: str | None = None) -> None:
    """Register a mock response for the Docker events endpoint."""
    if body is None:
        body = load_fixtures("docker_event.json")
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/{ENDPOINT_ID}/docker/events",
        "GET",
        aresponses.Response(
            status=status,
            headers={"Content-Type": "application/json"},
            text=body,
        ),
    )


async def test_event_listener_single_event(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that _listen delivers one event to the callback and then returns."""
    _events_response(aresponses)

    received: list[PortainerEventListenerResult] = []

    def my_callback(result: PortainerEventListenerResult) -> None:
        """Append result to the received list."""
        received.append(result)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(my_callback)
    await listener._listen(ENDPOINT_ID)

    assert len(received) == 1
    assert received[0].endpoint_id == ENDPOINT_ID
    assert received[0].event.type == "container"
    assert received[0].event.action == "start"
    assert received[0].event.actor is not None
    assert received[0].event.actor.id == CONTAINER_ID


async def test_event_listener_multiple_events(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that _listen delivers multiple events when the body contains several lines."""
    event_line = load_fixtures("docker_event.json").strip()
    body = f"{event_line}\n{event_line}\n{event_line}\n"
    _events_response(aresponses, body=body)

    received: list[PortainerEventListenerResult] = []

    def my_callback(result: PortainerEventListenerResult) -> None:
        """Append result to the received list."""
        received.append(result)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(my_callback)
    await listener._listen(ENDPOINT_ID)

    assert len(received) == 3


async def test_event_listener_start_stop(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that start() launches the task and stop() cancels it."""
    _events_response(aresponses)

    received: list[PortainerEventListenerResult] = []

    def my_callback(result: PortainerEventListenerResult) -> None:
        """Append result to the received list."""
        received.append(result)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(my_callback)

    assert listener._task is None

    listener.start()
    assert listener._task is not None
    assert not listener._task.done()

    await asyncio.sleep(0.05)

    listener.stop()
    # asyncio.gather inside _run needs a few loop iterations to fully cancel
    for _ in range(10):
        await asyncio.sleep(0)
    assert listener._task.done()

    assert len(received) >= 1


async def test_event_listener_start_idempotent(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that calling start() twice reuses the same task."""
    _events_response(aresponses)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.start()
    task_first = listener._task
    listener.start()
    assert listener._task is task_first

    listener.stop()
    await asyncio.sleep(0)


async def test_event_listener_sync_callback(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that a synchronous callback is invoked for each event."""
    _events_response(aresponses)

    received: list[PortainerEventListenerResult] = []

    def my_callback(result: PortainerEventListenerResult) -> None:
        """Append result to the received list."""
        received.append(result)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(my_callback)
    await listener._listen(ENDPOINT_ID)

    assert len(received) == 1


async def test_event_listener_async_callback(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that an async callback is awaited for each event."""
    _events_response(aresponses)

    received: list[PortainerEventListenerResult] = []

    async def my_async_callback(result: PortainerEventListenerResult) -> None:
        """Append result to the received list."""
        received.append(result)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(my_async_callback)
    await listener._listen(ENDPOINT_ID)

    assert len(received) == 1


async def test_event_listener_callback_duplicate_ignored(
    portainer_client: Portainer,
) -> None:
    """Test that registering the same callback twice only registers it once."""

    def my_callback(result: PortainerEventListenerResult) -> None:  # pylint: disable=unused-argument
        """Do nothing; used to test duplicate registration handling."""

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(my_callback)
    listener.register_callback(my_callback)

    assert listener._callbacks.count(my_callback) == 1


async def test_event_listener_unregister_callback(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that an unregistered callback is no longer called."""
    _events_response(aresponses)

    received: list[PortainerEventListenerResult] = []

    def my_callback(result: PortainerEventListenerResult) -> None:
        """Append result to the received list."""
        received.append(result)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(my_callback)
    listener.unregister_callback(my_callback)
    await listener._listen(ENDPOINT_ID)

    assert len(received) == 0


async def test_event_listener_callback_exception_logged(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that a callback exception is logged but does not stop the listener."""
    _events_response(aresponses)

    def bad_callback(result: PortainerEventListenerResult) -> None:  # noqa: ARG001  # pylint: disable=unused-argument
        """Raise an exception to test error handling."""
        msg = "boom"
        raise RuntimeError(msg)

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    listener.register_callback(bad_callback)

    with caplog.at_level(logging.ERROR):
        await listener._listen(ENDPOINT_ID)

    assert "Callback raised an exception" in caplog.text


@pytest.mark.parametrize(
    "status_code",
    [401, 404, 500],
)
async def test_event_listener_connection_error(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    status_code: int,
) -> None:
    """Test that HTTP errors from the events endpoint raise PortainerError subclasses."""
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/{ENDPOINT_ID}/docker/events",
        "GET",
        aresponses.Response(text="Error response", status=status_code),
    )

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)
    with pytest.raises(PortainerError):
        await listener._listen(ENDPOINT_ID)


async def test_event_listener_reconnects_on_connection_error(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that _listen_with_reconnect retries after a connection error."""
    # First call fails with a 500, second call succeeds
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/{ENDPOINT_ID}/docker/events",
        "GET",
        aresponses.Response(text="Error response", status=500),
    )
    _events_response(aresponses)

    received: list[PortainerEventListenerResult] = []

    def my_callback(result: PortainerEventListenerResult) -> None:
        """Append result to the received list."""
        received.append(result)

    listener = PortainerEventListener(
        portainer_client,
        endpoint_id=ENDPOINT_ID,
        reconnect_interval=timedelta(seconds=0),
    )
    listener.register_callback(my_callback)

    with caplog.at_level(logging.WARNING):
        # Run one reconnect cycle: fail → reconnect → succeed → return
        task = asyncio.create_task(listener._listen_with_reconnect(ENDPOINT_ID))
        await asyncio.sleep(0.1)
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    assert len(received) >= 1
    assert "reconnecting" in caplog.text.lower()


async def test_event_listener_auth_error_stops_listener(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that a 401 error stops the listener for that endpoint (no retry)."""
    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/{ENDPOINT_ID}/docker/events",
        "GET",
        aresponses.Response(text="Unauthorized", status=401),
    )

    listener = PortainerEventListener(portainer_client, endpoint_id=ENDPOINT_ID)

    with caplog.at_level(logging.ERROR):
        # _listen_with_reconnect should return (not loop) after an auth error
        await listener._listen_with_reconnect(ENDPOINT_ID)

    assert "Authentication error" in caplog.text


async def test_event_listener_event_type_filter(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that event_types are passed as filters to the events endpoint."""
    received_params: list[str] = []

    async def capturing_handler(request: Request) -> Response:
        """Capture the request URL for later inspection and return a dummy response."""
        received_params.append(str(request.rel_url))
        return Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_event.json"),
        )

    aresponses.add(
        "localhost:9000",
        f"/api/endpoints/{ENDPOINT_ID}/docker/events",
        "GET",
        capturing_handler,
    )

    listener = PortainerEventListener(
        portainer_client,
        endpoint_id=ENDPOINT_ID,
        event_types=["container"],
    )
    await listener._listen(ENDPOINT_ID)

    assert len(received_params) == 1
    assert "filters" in received_params[0]
    assert "container" in received_params[0]
