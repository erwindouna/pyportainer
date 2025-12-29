"""Asynchronous Python client for Python Portainer."""

from __future__ import annotations

import asyncio
import json
import socket
from dataclasses import dataclass
from datetime import timedelta
from importlib import metadata
from typing import Any, Self
from urllib.parse import urlparse

from aiohttp import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from pyportainer.exceptions import (
    PortainerAuthenticationError,
    PortainerConnectionError,
    PortainerError,
    PortainerNotFoundError,
    PortainerTimeoutError,
)
from pyportainer.models.docker import DockerContainer, DockerContainerStats, ImageInformation, LocalImageInformation
from pyportainer.models.docker_inspect import DockerInfo, DockerInspect, DockerVersion
from pyportainer.models.portainer import Endpoint

try:
    VERSION = metadata.version(__package__)
except metadata.PackageNotFoundError:  # pragma: no cover
    VERSION = "DEV-0.0.0"  # pylint: disable=invalid-name


@dataclass
class Portainer:
    """Main class for handling connections with the Python Portainer API."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    def __init__(
        self,
        api_url: str,
        api_key: str,
        *,
        request_timeout: float = 10.0,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize the Portainer object.

        Args:
        ----
            api_url: URL of the Portainer API.
            api_key: API key for authentication.
            request_timeout: Timeout for requests (in seconds).
            session: Optional aiohttp session to use.

        """
        self._api_key = api_key
        self._request_timeout = request_timeout
        self._session = session

        parsed_url = urlparse(api_url)
        self._api_host = parsed_url.hostname or "localhost"
        self._api_scheme = parsed_url.scheme or "http"
        self._api_port = parsed_url.port

    # pylint: disable=too-many-arguments, too-many-locals
    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        timeout: float | None = None,
        parse: bool = True,
    ) -> Any:
        """Handle a request to the Python Portainer API.

        Args:
        ----
            uri: Request URI, without '/api/', for example, 'status'.
            method: HTTP method to use.
            params: Extra options to improve or limit the response.
            timeout: Timeout for the request (in seconds).
            parse: Whether to parse the response as JSON.

        Returns:
        -------
            A Python dictionary (JSON decoded) with the response from
            the Python Portainer API.

        Raises:
        ------
            Python PortainerAuthenticationError: If the API key is invalid.

        """
        url = URL.build(
            scheme=self._api_scheme,
            host=self._api_host,
            port=self._api_port,
            path="/api/",
        ).join(URL(uri))

        headers = {
            "Accept": "application/json, text/plain",
            "User-Agent": f"PythonPortainer/{VERSION}",
            "X-API-Key": self._api_key,
        }

        if self._session is None:
            self._session = ClientSession()
            self._close_session = True

        # Only override timeout if a specific value is provided, else use default
        if timeout is None:
            timeout = self._request_timeout

        try:
            async with asyncio.timeout(timeout):
                response = await self._session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json_body,
                )
                response.raise_for_status()
        except TimeoutError as err:
            msg = f"Timeout error while accessing {method} {url}: {err}"
            raise PortainerTimeoutError(msg) from err
        except ClientResponseError as err:
            if err.status == 401:
                msg = f"Authentication failed for {method} {url}: Invalid API key"
                raise PortainerAuthenticationError(msg) from err
            if err.status == 404:
                msg = f"Resource not found at {method} {url}: {err}"
                raise PortainerNotFoundError(msg) from err
            msg = f"Connection error for {method} {url}: {err}"
            raise PortainerConnectionError(msg) from err
        except (ClientError, socket.gaierror) as err:
            msg = f"Unexpected error during {method} {url}: {err}"
            raise PortainerConnectionError(msg) from err

        if response.status in (204, 304):
            return None

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the Portainer API"
            raise PortainerError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        # Read events instead. Ideal for getting image pull progress
        events: list[Any] = []
        if not parse:
            async for chunk in response.content:
                for line in chunk.splitlines():
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue
                    events.append(json.loads(stripped_line))
            return events

        return await response.json()

    async def get_endpoints(self) -> list[Endpoint]:
        """Get the list of endpoints from the Portainer API.

        Returns
        -------
            A list of Endpoint objects.

        """
        endpoints = await self._request("endpoints")

        return [Endpoint.from_dict(endpoint) for endpoint in endpoints]

    async def get_containers(self, endpoint_id: int) -> list[DockerContainer]:
        """Get the list of containers from the Portainer API.

        Args:
        ----
            endpoint_id: The ID of the endpoint to get containers from.
            all: If True, include all containers. If False, only running containers.

        Returns:
        -------
            A list of containers.

        """
        containers = await self._request(f"endpoints/{endpoint_id}/docker/containers/json?all=1")

        return [DockerContainer.from_dict(container) for container in containers]

    async def start_container(self, endpoint_id: int, container_id: str) -> Any:
        """Start a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to start.

        """
        return await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}/start",
            method="POST",
        )

    async def stop_container(self, endpoint_id: int, container_id: str) -> Any:
        """Stop a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to stop.

        """
        return await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}/stop",
            method="POST",
        )

    async def restart_container(self, endpoint_id: int, container_id: str) -> Any:
        """Restart a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to restart.

        """
        return await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}/restart",
            method="POST",
        )

    async def pause_container(self, endpoint_id: int, container_id: str) -> Any:
        """Pause a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to pause.

        """
        return await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}/pause",
            method="POST",
        )

    async def unpause_container(self, endpoint_id: int, container_id: str) -> Any:
        """Unpause a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to unpause.

        """
        return await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}/unpause",
            method="POST",
        )

    async def kill_container(self, endpoint_id: int, container_id: str) -> Any:
        """Kill a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to kill.

        """
        return await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}/kill",
            method="POST",
        )

    async def delete_container(self, endpoint_id: int, container_id: str, *, force: bool = False) -> Any:
        """Delete a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to delete.
            force: If True, force delete the container.

        """
        params = {"force": str(force).lower()}
        return await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}",
            method="DELETE",
            params=params,
        )

    async def inspect_container(self, endpoint_id: int, container_id: str, *, raw: bool = False) -> DockerInspect | Any:
        """Inspect a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to inspect.
            raw: If True, return the raw JSON response. If False, return a DockerInspect object.

        Returns:
        -------
            A DockerContainer object with the inspected data.

        """
        container = await self._request(f"endpoints/{endpoint_id}/docker/containers/{container_id}/json")

        if raw:
            return container
        return DockerInspect.from_dict(container)

    async def docker_version(self, endpoint_id: int) -> DockerVersion:
        """Get the Docker version on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.

        Returns:
        -------
            A DockerVersion object with the Docker version data.

        """
        version = await self._request(f"endpoints/{endpoint_id}/docker/version")

        return DockerVersion.from_dict(version)

    async def docker_info(self, endpoint_id: int) -> DockerInfo:
        """Get the Docker info on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.

        Returns:
        -------
            A DockerInfo object with the Docker info data.

        """
        info = await self._request(f"endpoints/{endpoint_id}/docker/info")

        return DockerInfo.from_dict(info)

    async def container_stats(
        self,
        endpoint_id: int,
        container_id: str,
        *,
        stream: bool = False,
        one_shot: bool = True,
    ) -> Any:
        """Get the stats of a container on the specified endpoint.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to get stats from.
            stream: If True, stream the stats. If False, get a single snapshot.
            one_shot: If True, get a single snapshot. If False, stream the stats.

        Returns:
        -------
            The stats of the container.

        """
        params = {"stream": str(stream).lower(), "one-shot": str(one_shot).lower()}
        stats = await self._request(
            f"endpoints/{endpoint_id}/docker/containers/{container_id}/stats",
            params=params,
        )

        return DockerContainerStats.from_dict(stats)

    async def get_image_information(self, endpoint_id: int, image_id: str) -> ImageInformation:
        """Get information about a Docker image.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            image_id: The ID of the image to get information about.

        Returns:
        -------
            An ImageInformation object with the image data.

        """
        image = await self._request(f"endpoints/{endpoint_id}/docker/distribution/{image_id}/json")

        return ImageInformation.from_dict(image)

    async def get_image(self, endpoint_id: int, image_id: str) -> LocalImageInformation:
        """Get information about a Docker image.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            image_id: The ID of the image to get information about.

        Returns:
        -------
            A LocalImageInformation object with the image data.

        """
        image = await self._request(f"endpoints/{endpoint_id}/docker/images/{image_id}/json")

        return LocalImageInformation.from_dict(image)

    async def image_recreate(self, endpoint_id: int, image_id: str, timeout: timedelta = timedelta(minutes=5)) -> Any:
        """Recreate a Docker image.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            image_id: The ID of the image to recreate.
            timeout: Timeout for the image recreation process. Defaults to 5 minutes.

        Returns:
        -------
            An ImageInformation object with the recreated image data.

        """
        params = {"fromImage": image_id}
        return await self._request(
            uri=f"endpoints/{endpoint_id}/docker/images/create?fromImage={image_id}",
            timeout=timeout.total_seconds(),
            method="POST",
            params=params,
            parse=False,
        )

    async def container_recreate_helper(self, endpoint_id: int, container_id: str, image: str, timeout: timedelta = timedelta(minutes=5)) -> Any:
        """Recreate a Docker container service.

        This helper runs through the Portainer API and recreates the specified container.
        It first inspects the container to get its configuration, then creates a new container
        with the same configuration.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to recreate.
            image: The tag of the image to use for the new container.

        Returns:
        -------
            The response from the Portainer API.

        """
        container_inspect = await self.inspect_container(
            endpoint_id=endpoint_id,
            container_id=container_id,
            raw=True,
        )

        if not isinstance(container_inspect, dict):
            msg = "Failed to inspect container for recreation."
            raise PortainerError(msg)

        await self.image_recreate(
            endpoint_id=endpoint_id,
            image_id=image,
            timeout=timeout,
        )

        await self.stop_container(
            endpoint_id=endpoint_id,
            container_id=container_id,
        )

        await self.delete_container(
            endpoint_id=endpoint_id,
            container_id=container_id,
            force=True,
        )

        create_body = {
            **container_inspect["Config"],
            "Image": image,
            "HostConfig": container_inspect["HostConfig"],
            "Config": container_inspect["Config"],
        }

        created = await self.container_create(
            endpoint_id=endpoint_id,
            name=container_inspect.get("Name", "").lstrip("/"),
            image=image,
            config=create_body,
        )

        # This is optional; reattach networks the same way as the original container
        # I have to test this, probablt need some friendly users...
        networks = (container_inspect["NetworkSettings"] or {}).get("Networks") or {}
        for net_name in networks:
            network_name = (container_inspect["HostConfig"] or {}).get("NetworkMode") or ""
            if network_name in {"host", "none"} or network_name.startswith("container:"):
                continue

            await self._request(
                f"endpoints/{endpoint_id}/docker/networks/{net_name}/connect",
                method="POST",
                json_body={"Container": created.id},
            )

        await self.start_container(
            endpoint_id=endpoint_id,
            container_id=created.id,
        )

        return created

    async def container_recreate(
        self, endpoint_id: int, container_id: str, timeout: timedelta = timedelta(minutes=5), *, pull_image: bool = False
    ) -> DockerContainer:
        """Recreate a Docker container.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            container_id: The ID of the container to recreate.
            timeout: Timeout for the container recreation process. Defaults to 5 minutes.
            pull_image: If True, pull the latest image before recreating the container.

        Returns:
        -------
            The response from the Portainer API.

        """
        params = {"PullImage": pull_image}
        container = await self._request(
            uri=f"docker/{endpoint_id}/containers/{container_id}/recreate",
            method="POST",
            json_body=params,
            timeout=timeout.total_seconds(),
        )

        return DockerContainer.from_dict(container)

    async def container_create(self, endpoint_id: int, name: str, image: str, config: dict[str, Any]) -> DockerContainer:
        """Create a Docker container.

        Args:
        ----
            endpoint_id: The ID of the endpoint.
            name: The name of the container to create.

        Returns:
        -------
            A DockerContainer object with the created container data.

        """
        params = {"name": name}
        json_body = {"Image": image}
        json_body.update(config)
        container = await self._request(
            uri=f"endpoints/{endpoint_id}/docker/containers/create",
            method="POST",
            params=params,
            json_body=json_body,
        )

        return DockerContainer.from_dict(container)

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The Portainer object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
