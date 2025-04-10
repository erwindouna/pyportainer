"""Data models for Swarm operations in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class ServiceUpdateResponse(DataClassDictMixin):
    """Response for updating a Swarm service."""

    warnings: list[str] | None = Field(None, alias="Warnings")
