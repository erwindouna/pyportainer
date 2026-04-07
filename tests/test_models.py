"""Test the models of the Portainer API."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from aresponses import ResponsesMockServer
from freezegun import freeze_time
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


async def test_portainer_system_status(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer system status."""
    aresponses.add(
        "localhost:9000",
        "/api/system/status",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("portainer_system_status.json"),
        ),
    )

    system_status = await portainer_client.portainer_system_status()
    assert system_status == snapshot


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
    snapshot: SnapshotAssertion,
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

    status = await portainer_client.container_image_status(endpoint_id=1, image="nginx:latest")
    assert status == snapshot


async def test_container_image_status_up_to_date(
    aresponses: ResponsesMockServer,
    portainer_client: Portainer,
    snapshot: SnapshotAssertion,
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

    status = await portainer_client.container_image_status(endpoint_id=1, image="nginx:latest")
    assert status == snapshot


async def test_portainer_volumes(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer volumes."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/volumes",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("volumes.json"),
        ),
    )

    volumes = await portainer_client.get_volumes(1)
    assert volumes == snapshot


async def test_portainer_volume_inspect(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer volume inspect."""
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/volumes/tardis",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("volume_inspect.json"),
        ),
    )

    volume = await portainer_client.inspect_volume(1, "tardis")
    assert volume == snapshot


async def test_get_container_cpu_usage(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test the Portainer get_container_cpu_usage."""
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

    cpu_usage = await portainer_client.get_container_cpu_usage(endpoint_id=1, container_id="test_container")
    assert cpu_usage == snapshot


async def test_get_container_cpu_usage_with_percentage(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    portainer_client: Portainer,
) -> None:
    """Test that CPU percentages are calculated correctly on the second call."""
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
    aresponses.add(
        "localhost:9000",
        "/api/endpoints/1/docker/containers/test_container/stats",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("container_stats_2.json"),
        ),
    )

    with freeze_time("2015-01-08T22:57:31Z"):
        await portainer_client.get_container_cpu_usage(endpoint_id=1, container_id="test_container")

    with freeze_time("2015-01-08T22:57:32Z"):
        cpu_usage = await portainer_client.get_container_cpu_usage(endpoint_id=1, container_id="test_container")

    assert cpu_usage == snapshot
