"""Data models for resource-related types in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class Quantity(DataClassDictMixin):
    """Represents a resource quantity."""

    format: str | None = Field(None, alias="Format")
