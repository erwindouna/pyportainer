"""Data models for container-related operations."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class ContainerGpusResponse(DataClassDictMixin):
    """Response containing GPU information for a container."""

    gpus: str | None = None


class ContainerPayload(DataClassDictMixin):
    """Payload for creating or updating a container."""

    container_id: str | None = Field(default=None, alias="containerID")
