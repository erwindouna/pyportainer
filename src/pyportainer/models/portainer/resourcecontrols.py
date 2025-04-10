"""Data models for resource control operations in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class ResourceControlCreatePayload(DataClassDictMixin):
    """Payload for creating a resource control."""

    administrators_only: bool | None = Field(None, alias="administratorsOnly")
    public: bool | None = Field(None)
    resource_id: str = Field(..., alias="resourceID")
    sub_resource_i_ds: list[str] | None = Field(None, alias="subResourceIDs")
    teams: list[int] | None = Field(None)
    type: int = Field(...)
    users: list[int] | None = Field(None)


class ResourceControlUpdatePayload(DataClassDictMixin):
    """Payload for updating a resource control."""

    administrators_only: bool | None = Field(None, alias="administratorsOnly")
    public: bool | None = Field(None)
    teams: list[int] | None = Field(None)
    users: list[int] | None = Field(None)
