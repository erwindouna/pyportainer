"""Conftest for the pyportainer tests."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession

from pyportainer import Portainer


@pytest.fixture(name="portainer_client")
async def client() -> AsyncGenerator[Portainer, None]:
    """Return a pyportainer client."""
    async with (
        ClientSession() as session,
        Portainer(
            api_url="http://localhost:9000/api",
            api_key="test_api_key",
            session=session,
            request_timeout=10.0,
        ) as portainer_client,
    ):
        yield portainer_client
