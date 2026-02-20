"""Test the models of the Portainer API."""

from __future__ import annotations

from datetime import timedelta
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


async def test_portainer_container_inspect(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer container inspect."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/test_container/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("container_inspect.json"),
        ),
    )

    container = await portainer_client.inspect_container(1, "test_container")
    assert container == snapshot


async def test_portainer_docker_version(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer Docker version."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/version",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_version.json"),
        ),
    )

    docker_version = await portainer_client.docker_version(endpoint_id=1)
    assert docker_version == snapshot


async def test_portainer_docker_info(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer Docker info."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/info",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_info.json"),
        ),
    )

    docker_info = await portainer_client.docker_info(endpoint_id=1)
    assert docker_info == snapshot


async def test_portainer_container_stats(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer container stats."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/test_container/stats",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("container_stats.json"),
        ),
    )

    container_stats = await portainer_client.container_stats(1, "test_container")
    assert container_stats == snapshot


async def test_portainer_images(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer images."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/distribution/image_id/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )

    images = await portainer_client.get_image_information(endpoint_id=1, image_id="image_id")
    assert images == snapshot


async def test_portainer_local_images(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer local images."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/images/image_id/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    local_images = await portainer_client.get_image(endpoint_id=1, image_id="image_id")
    assert local_images == snapshot


async def test_portainer_images_prune(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer prune images."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/images/prune",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_image_prune.json"),
        ),
    )

    prune_response = await portainer_client.images_prune(
        endpoint_id=1,
        dangling=True,
        until=timedelta(hours=1),
    )
    assert prune_response == snapshot


async def test_portainer_system_df(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer system df."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/system/df",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("docker_system_df.json"),
        ),
    )

    system_df = await portainer_client.docker_system_df(endpoint_id=1)
    assert system_df == snapshot


async def test_container_image_status_update_available(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test container_image_status when the registry digest differs from the local digest."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/distribution/nginx:latest/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/images/nginx:latest/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    status = await portainer_client.container_image_status(endpoint_id=1, image_id="nginx:latest")
    assert status.update_available is True
    assert status.registry_digest == "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96"


async def test_container_image_status_up_to_date(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
) -> None:
    """Test container_image_status when the registry digest matches the local digest."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/distribution/nginx:latest/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("image_information_up_to_date.json"),
        ),
    )
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/images/nginx:latest/json",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("local_image_information.json"),
        ),
    )

    status = await portainer_client.container_image_status(endpoint_id=1, image_id="nginx:latest")
    assert status.update_available is False
    assert status.registry_digest == "sha256:afcc7f1ac1b49db317a7196c902e61c6c3c4607d63599ee1a82d702d249a0ccb"
