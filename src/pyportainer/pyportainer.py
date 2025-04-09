"""Asynchronous Python client for Python Portainer."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self
from urllib.parse import urlparse

import aiohttp
from aiohttp import ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from pyportainer.exceptions import (
    PortainerAuthenticationError,
    PortainerConnectionError,
    PortainerError,
    PortainerNotFoundError,
    PortainerTimeoutError,
)

try:
    VERSION = metadata.version(__package__)
except metadata.PackageNotFoundError:
    VERSION = "DEV-0.0.0"


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
        self._api_port = parsed_url.port or 9000

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Python Portainer API.

        Args:
        ----
            uri: Request URI, without '/api/', for example, 'status'.
            method: HTTP method to use.
            params: Extra options to improve or limit the response.

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

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with asyncio.timeout(self._request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                )
                response.raise_for_status()
        except TimeoutError as err:
            msg = f"Timeout error while accessing {method} {url}: {err}"
            raise PortainerTimeoutError(msg) from err
        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                msg = f"Authentication failed for {method} {url}: Invalid API key"
                raise PortainerAuthenticationError(msg) from err
            if err.status == 404:
                msg = f"Resource not found at {method} {url}: {err}"
                raise PortainerNotFoundError(msg) from err
            msg = f"Connection error for {method} {url}: {err}"
            raise PortainerConnectionError(msg) from err
        except Exception as err:
            msg = f"Unexpected error during {method} {url}: {err}"
            raise PortainerConnectionError(msg) from err

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the Portainer API"
            raise PortainerError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def get_endpoints(self) -> Any:
        """Get the list of endpoints from the Portainer API.

        Returns
        -------
            A list of endpoints.

        """
        endpoints = await self._request("endpoints")

        if endpoints is None:
            msg = "No endpoints found in the Portainer API"
            raise PortainerError(msg, {"response": endpoints})

        return endpoints

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

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
