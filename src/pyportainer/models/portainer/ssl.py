"""Data models for SSL configuration in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class SslUpdatePayload(DataClassDictMixin):
    """Payload for updating SSL configuration."""

    cert: str | None = Field(None)
    httpenabled: bool | None = None
    key: str | None = None
