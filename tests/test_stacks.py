"""Tests for Portainer stacks API."""

from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from pyportainer import Portainer
from pyportainer.models.stacks import StackStatus, StackType
from tests import load_fixtures


async def test_get_stacks(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test getting all stacks."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stacks.json"),
        ),
    )
    stacks = await portainer_client.get_stacks()
    assert stacks == snapshot


async def test_get_stacks_with_endpoint_filter(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test getting stacks filtered by endpoint ID."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stacks.json"),
        ),
        match_querystring=False,
    )
    stacks = await portainer_client.get_stacks(endpoint_id=1)
    assert len(stacks) == 3


async def test_get_stacks_with_swarm_filter(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test getting stacks filtered by Swarm ID."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='[{"Id": 3, "Name": "swarm-service", "Type": 1, "EndpointId": 1, "Status": 1, "SwarmId": "jpofkc0i9uo9wtx1zesuk649w"}]',
        ),
        match_querystring=False,
    )
    stacks = await portainer_client.get_stacks(swarm_id="jpofkc0i9uo9wtx1zesuk649w")
    assert len(stacks) == 1
    assert stacks[0].swarm_id == "jpofkc0i9uo9wtx1zesuk649w"


async def test_get_stacks_empty(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test getting stacks when no stacks exist (204 response)."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks",
        "GET",
        aresponses.Response(
            status=204,
            headers={"Content-Type": "application/json"},
        ),
    )
    stacks = await portainer_client.get_stacks()
    assert stacks == []


async def test_get_stack(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test getting a specific stack."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stack.json"),
        ),
    )
    stack = await portainer_client.get_stack(stack_id=1)
    assert stack == snapshot


async def test_get_stack_containers(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test getting containers in a stack."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("containers.json"),
        ),
        match_querystring=False,
    )
    containers = await portainer_client.get_stack_containers(
        endpoint_id=1,
        stack_name="my-web-app",
    )
    assert containers == snapshot


async def test_start_stack(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test starting a stopped stack."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1/start",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stack.json"),
        ),
        match_querystring=False,
    )
    stack = await portainer_client.start_stack(stack_id=1, endpoint_id=1)
    assert stack == snapshot


async def test_stop_stack(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test stopping a running stack."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1/stop",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stack_stopped.json"),
        ),
        match_querystring=False,
    )
    stack = await portainer_client.stop_stack(stack_id=1, endpoint_id=1)
    assert stack == snapshot


async def test_delete_stack(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test deleting a stack."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1",
        "DELETE",
        aresponses.Response(
            status=204,
            headers={"Content-Type": "application/json"},
        ),
        match_querystring=False,
    )
    await portainer_client.delete_stack(stack_id=1, endpoint_id=1)


async def test_delete_stack_external(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test deleting an external Swarm stack."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1",
        "DELETE",
        aresponses.Response(
            status=204,
            headers={"Content-Type": "application/json"},
        ),
        match_querystring=False,
    )
    await portainer_client.delete_stack(stack_id=1, endpoint_id=1, external=True)


async def test_stack_status_enum() -> None:
    """Test StackStatus enum values."""
    assert StackStatus.ACTIVE == 1
    assert StackStatus.INACTIVE == 2
    assert StackStatus(1) == StackStatus.ACTIVE
    assert StackStatus(2) == StackStatus.INACTIVE


async def test_stack_type_enum() -> None:
    """Test StackType enum values."""
    assert StackType.SWARM == 1
    assert StackType.COMPOSE == 2
    assert StackType.KUBERNETES == 3
    assert StackType(1) == StackType.SWARM
    assert StackType(2) == StackType.COMPOSE
    assert StackType(3) == StackType.KUBERNETES
