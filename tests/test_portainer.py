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
