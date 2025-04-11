"""Test the models of the Portainer API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from tests import load_fixtures

if TYPE_CHECKING:
    from pyportainer import Portainer
    from pyportainer.models.portainer import Endpoint


async def test_portainer_endpoints(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer endpoints."""
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

    endpoints: list[Endpoint] = await portainer_client.get_endpoints()
    assert endpoints == snapshot


async def test_portainer_containers(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer containers."""
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

    containers = await portainer_client.get_containers(1)
    assert containers == snapshot
