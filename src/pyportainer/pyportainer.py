"""Asynchronous Python client for Python Portainer."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self, cast

from aiohttp import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import
from .models import

VERSION = metadata.version(__package__)


@dataclass
class ...
    """Main class for handling connections with the Python Portainer API."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

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

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The Powerfox object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
