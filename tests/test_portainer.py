"""Basic tests for the pyportainer library."""

# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse, ClientSession
from aresponses import Response, ResponsesMockServer

from pyportainer import Portainer
from pyportainer.exceptions import (
    PortainerAuthenticationError,
    PortainerConnectionError,
    PortainerError,
    PortainerNotFoundError,
    PortainerTimeoutError,
)
from pyportainer.models.docker import DockerContainer
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

    async with Portainer(api_url="http://localhost:9000/api", api_key="test-api-key") as client:
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
        client = Portainer(api_url="http://localhost:9000/api", api_key="test_api_key", session=session, request_timeout=0.1)
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
        client = Portainer(api_url="http://localhost:9000/api", api_key="test_api_key", session=session)
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
