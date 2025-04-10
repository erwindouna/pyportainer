"""Data models for team management in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class TeamCreatePayload(DataClassDictMixin):
    """Payload for creating a team."""

    name: str = Field(...)
    team_leaders: list[int] | None = Field(None, alias="teamLeaders")


class TeamUpdatePayload(DataClassDictMixin):
    """Payload for updating a team."""

    name: str | None = Field(None)
