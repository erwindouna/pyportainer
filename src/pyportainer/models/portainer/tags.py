"""Data models for tag management in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class TagPayload(DataClassDictMixin):
    """Payload for creating or updating a tag."""

    id: int | None = Field(default=None, alias="id")
    name: str | None = Field(default=None, alias="name")
