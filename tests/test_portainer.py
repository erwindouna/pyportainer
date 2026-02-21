"""Basic tests for the pyportainer library."""

# pylint: disable=protected-access
import asyncio
from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse, ClientSession
from aiohttp.web import Request
from aresponses import Response, ResponsesMockServer

from pyportainer import Portainer
from pyportainer.exceptions import (
    PortainerAuthenticationError,
    PortainerConnectionError,
    PortainerError,
    PortainerNotFoundError,
    PortainerTimeoutError,
)
from pyportainer.models.docker import DockerContainer, DockerEvent
from tests import load_fixtures


async def test_json_request(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "localhost:9000",
        "/api/test",
        "GET",
        aresponses.Response(status=200, headers={"Content-Type": "application/json"}, text="{}"),
    )
    response = await portainer_client._request("test")
    assert response is not None
    await portainer_client.close()


async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test internal session is created and closed."""
    aresponses.add(
        "localhost:9000",
        "/api/test",
        "GET",
        aresponses.Response(status=200, headers={"Content-Type": "application/json"}, text="{}"),
    )

    async with Portainer(api_url="http://localhost:9000", api_key="test-api-key") as client:
        response = await client._request("test")
        assert response == {}


async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout from Portainer API."""

    # Faking a timeout by sleeping
    async def response_handler(_: ClientResponse) -> Response:
        await asyncio.sleep(0.2)
        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="{}",
        )

    aresponses.add(
        "localhost:9000",
        "/api/test",
        "GET",
        response_handler,
    )

    async with ClientSession() as session:
        client = Portainer(api_url="http://localhost:9000", api_key="test_api_key", session=session, request_timeout=0.1)
        with pytest.raises(PortainerTimeoutError):
            await client._request("test")
        await session.close()


async def test_content_type(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test request content type error from Portainer API."""
    aresponses.add(
        "localhost:9000",
        "/api/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )
    with pytest.raises(PortainerError):
        assert await portainer_client._request("test")


async def test_client_error() -> None:
    """Test request client error from Autarco API."""
    async with ClientSession() as session:
        client = Portainer(api_url="http://localhost:9000", api_key="test_api_key", session=session)
        with (
            patch.object(
                session,
                "request",
                side_effect=ClientError,
            ),
            pytest.raises(PortainerConnectionError),
        ):
            assert await client._request("test")
        await session.close()


@pytest.mark.parametrize(
    ("status_code", "expected_exception"),
    [
        (401, PortainerAuthenticationError),
        (404, PortainerNotFoundError),
        (500, PortainerConnectionError),
    ],
)
async def test_response_status(
    aresponses: ResponsesMockServer, portainer_client: Portainer, status_code: int, expected_exception: type[Exception]
) -> None:
    """Test HTTP response status handling."""
    aresponses.add(
        "localhost:9000",
        "/api/test",
        "GET",
        aresponses.Response(text="Error response", status=status_code),
    )
    with pytest.raises(expected_exception):
        await portainer_client._request("test")


async def test_start_container(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test starting a container."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/start",
        "POST",
        aresponses.Response(status=204),
    )
    response = await portainer_client.start_container(1, "container_id")
    assert response is None


async def test_stop_container(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test stopping a container."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/stop",
        "POST",
        aresponses.Response(status=304),
    )
    response = await portainer_client.stop_container(1, "container_id")
    assert response is None


async def test_restart_container(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test restarting a container."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/restart",
        "POST",
        aresponses.Response(status=204),
    )
    response = await portainer_client.restart_container(1, "container_id")
    assert response is None


async def test_pause_container(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test pausing a container."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/pause",
        "POST",
        aresponses.Response(status=204),
    )
    response = await portainer_client.pause_container(1, "container_id")
    assert response is None


async def test_unpause_container(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test unpausing a container."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/unpause",
        "POST",
        aresponses.Response(status=204),
    )
    response = await portainer_client.unpause_container(1, "container_id")
    assert response is None


async def test_kill_container(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test killing a container."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/kill",
        "POST",
        aresponses.Response(status=204),
    )
    response = await portainer_client.kill_container(1, "container_id")
    assert response is None


async def test_delete_container(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test deleting a container."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id",
        "DELETE",
        aresponses.Response(status=204),
    )
    response = await portainer_client.delete_container(1, "container_id")
    assert response is None


async def test_image_recreate(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test recreating an image."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/images/create",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="""
                {"status": "Pulling from adguard/adguardhome", "id": "latest"}
                {"status": "Digest: sha256:09a24f05e110e53e213a340b22e5d3c8cdab12ff9be6775388c71b140255c54c"}
                {"status": "Status: Image is up to date for adguard/adguardhome:latest"}
            """,
        ),
    )
    response = await portainer_client.image_recreate(1, "adguard/adguardhome:latest")
    assert isinstance(response, list)
    assert response[0]["status"] == "Pulling from adguard/adguardhome"


async def test_container_recreate_helper(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test container recreate helper."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("container_inspect.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/images/create",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="""
                {"status": "Pulling from adguard/adguardhome", "id": "latest"}
                {"status": "Digest: sha256:09a24f05e110e53e213a340b22e5d3c8cdab12ff9be6775388c71b140255c54c"}
                {"status": "Status: Image is up to date for adguard/adguardhome:latest"}
            """,
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id/stop",
        "POST",
        aresponses.Response(
            status=204,
            headers={"Content-Type": "application/json"},
            text="",
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/funny_chatelet/start",
        "POST",
        aresponses.Response(
            status=204,
            headers={"Content-Type": "application/json"},
            text="",
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/container_id",
        "DELETE",
        aresponses.Response(status=204),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/create",
        "POST",
        aresponses.Response(
            status=201,
            headers={"Content-Type": "application/json"},
            text='{"Id": "funny_chatelet"}',
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/networks/property1/connect",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="",
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/networks/property2/connect",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text="",
        ),
    )

    response = await portainer_client.container_recreate_helper(1, "container_id", "adguard/adguardhome:latest")
    assert isinstance(response, DockerContainer)


async def test_container_recreate(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test container recreate."""
    aresponses.add(
        "localhost:9000",
        "/api/docker/1/containers/container_id/recreate",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("container_inspect.json"),
        ),
    )

    response = await portainer_client.container_recreate(1, "container_id")
    assert isinstance(response, DockerContainer)


async def test_get_recent_events(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that get_recent_events returns a list of DockerEvent objects."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/events",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_event.json"),
        ),
    )

    since = datetime(2023, 11, 14, tzinfo=UTC)
    until = datetime(2023, 11, 15, tzinfo=UTC)
    events = await portainer_client.get_recent_events(1, since=since, until=until)

    assert isinstance(events, list)
    assert len(events) == 1
    assert isinstance(events[0], DockerEvent)
    assert events[0].type == "container"
    assert events[0].action == "start"


async def test_get_recent_events_until_defaults_to_now(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that get_recent_events defaults until to the current time."""
    received_params: list[str] = []

    async def capturing_handler(request: Request) -> aresponses.Response:
        """Capture query params and return a single event."""
        received_params.append(str(request.rel_url))
        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_event.json"),
        )

    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/events",
        "GET",
        capturing_handler,
    )

    since = datetime(2023, 11, 14, tzinfo=UTC)
    await portainer_client.get_recent_events(1, since=since)

    assert len(received_params) == 1
    assert "since" in received_params[0]
    assert "until" in received_params[0]


async def test_get_events_since_until_params(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that get_events passes since/until as Unix timestamps."""
    received_params: list[str] = []

    async def capturing_handler(request: Request) -> aresponses.Response:
        """Capture query params and return a single event."""
        received_params.append(str(request.rel_url))
        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_event.json"),
        )

    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/events",
        "GET",
        capturing_handler,
    )

    since = datetime(2023, 11, 14, tzinfo=UTC)
    until = datetime(2023, 11, 15, tzinfo=UTC)
    async for _ in portainer_client.get_events(1, since=since, until=until):
        pass

    assert len(received_params) == 1
    assert f"since={int(since.timestamp())}" in received_params[0]
    assert f"until={int(until.timestamp())}" in received_params[0]


async def test_get_events_with_filters(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test that get_events passes filters as a JSON-encoded query param."""
    received_params: list[str] = []

    async def capturing_handler(request: Request) -> aresponses.Response:
        """Capture query params and return a single event."""
        received_params.append(str(request.rel_url))
        return aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_event.json"),
        )

    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/events",
        "GET",
        capturing_handler,
    )

    filters = {"type": ["container"], "event": ["start", "die"]}
    async for _ in portainer_client.get_events(1, filters=filters):
        pass

    assert len(received_params) == 1
    assert "filters" in received_params[0]
    # The filter values should be URL-encoded in the query string
    assert "container" in received_params[0]
