"""Conftest for the pyportainer tests."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession
from syrupy.assertion import SnapshotAssertion

from pyportainer import Portainer

from .syrupy import PortainerSnapshotExtension


@pytest.fixture(name="snapshot")
def snapshot_assertion(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Portainer extension."""
    return snapshot.use_extension(PortainerSnapshotExtension)


@pytest.fixture(name="portainer_client")
async def client() -> AsyncGenerator[Portainer, None]:
    """Return a pyportainer client."""
    async with (
        ClientSession() as session,
        Portainer(
            api_url="http://localhost:9000",
            api_key="test_api_key",
            session=session,
            request_timeout=10.0,
            max_retries=0,
        ) as portainer_client,
    ):
        yield portainer_client
