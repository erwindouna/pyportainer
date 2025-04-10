"""Data models for team membership management in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic.fields import Field


class TeamMembershipCreatePayload(DataClassDictMixin):
    """Payload for creating a team membership."""

    role: int = Field(...)
    team_id: int = Field(..., alias="teamID")
    user_id: int = Field(..., alias="userID")


class TeamMembershipUpdatePayload(DataClassDictMixin):
    """Payload for updating a team membership."""

    role: int = Field(...)
    team_id: int = Field(..., alias="teamID")
    user_id: int = Field(..., alias="userID")
