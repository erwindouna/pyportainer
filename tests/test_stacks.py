"""Tests for Portainer stacks API."""

from collections.abc import Awaitable, Callable
from typing import Any

import pytest
from aiohttp.web import Request, Response
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from pyportainer import Portainer, PortainerError
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
    snapshot: SnapshotAssertion,
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
    assert stacks == snapshot


async def test_get_stacks_with_swarm_filter(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
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
    assert stacks == snapshot


async def test_get_stacks_empty(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
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
    assert stacks == snapshot


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


async def test_get_stack_file(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test getting the stack file of a stack."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1/file",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stack_file.json"),
        ),
    )
    stack_file = await portainer_client.get_stack_file(stack_id=1)
    assert stack_file == "services:\n  web:\n    image: nginx:latest\n"


def _capture_update(captured: dict[str, Any]) -> Callable[[Request], Awaitable[Response]]:
    """Return an aresponses handler that records the update request."""

    async def handler(request: Request) -> Response:
        captured["endpoint_id"] = request.query.get("endpointId")
        captured["body"] = await request.json()
        return Response(
            status=200,
            content_type="application/json",
            text=load_fixtures("stack.json"),
        )

    return handler


@pytest.mark.parametrize(
    ("kwargs", "expected_flags"),
    [
        pytest.param(
            {},
            {"Prune": False, "RepullImageAndRedeploy": True, "PullImage": True},
            id="defaults",
        ),
        pytest.param(
            {"pull_image": False, "prune": True},
            {"Prune": True, "RepullImageAndRedeploy": False, "PullImage": False},
            id="overrides",
        ),
    ],
)
async def test_update_stack_file_based(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
    kwargs: dict[str, Any],
    expected_flags: dict[str, bool],
) -> None:
    """Test a file-based stack is redeployed with its current file and env vars."""
    captured: dict[str, Any] = {}
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
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1/file",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stack_file.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/stacks/1",
        "PUT",
        _capture_update(captured),
        match_querystring=False,
    )

    stack = await portainer_client.update_stack(endpoint_id=1, stack_id=1, **kwargs)

    assert stack == snapshot
    assert captured["endpoint_id"] == "1"
    # Portainer replaces the env vars and prune setting with what the update sends.
    assert captured["body"] == {
        "StackFileContent": "services:\n  web:\n    image: nginx:latest\n",
        "Env": [
            {"name": "NODE_ENV", "value": "production"},
            {"name": "PORT", "value": "3000"},
        ],
        **expected_flags,
    }


@pytest.mark.parametrize(
    ("kwargs", "expected_body"),
    [
        pytest.param(
            {},
            {"RepullImageAndRedeploy": True, "PullImage": True},
            id="defaults",
        ),
        pytest.param(
            {"prune": True},
            {"RepullImageAndRedeploy": True, "PullImage": True, "Prune": True},
            id="prune",
        ),
    ],
)
async def test_update_stack_git(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    kwargs: dict[str, Any],
    expected_body: dict[str, Any],
) -> None:
    """Test a Git stack is redeployed from its repository, keeping its env vars."""
    captured: dict[str, Any] = {}
    aresponses.add(
        "localhost:9000",
        "/api/stacks/2",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stack_git.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/stacks/2/git/redeploy",
        "PUT",
        _capture_update(captured),
        match_querystring=False,
    )

    await portainer_client.update_stack(endpoint_id=1, stack_id=2, **kwargs)

    assert captured["endpoint_id"] == "1"
    assert captured["body"] == expected_body


async def test_update_stack_kubernetes(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test updating a Kubernetes stack raises an error."""
    aresponses.add(
        "localhost:9000",
        "/api/stacks/3",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("stack_kubernetes.json"),
        ),
    )
    with pytest.raises(PortainerError, match="Kubernetes"):
        await portainer_client.update_stack(endpoint_id=1, stack_id=3)
