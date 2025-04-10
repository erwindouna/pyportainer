"""Data models for Docker images in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class ImageResponse(DataClassDictMixin):
    """Response containing details of a Docker image."""

    created: int | None = None
    id: str | None = None
    node_name: str | None = Field(None, alias="nodeName")
    size: int | None = None
    tags: list[str] | None = None
    used: bool | None = Field(None)
