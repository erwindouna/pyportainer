"""Data models for endpoint groups in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class EndpointGroupCreatePayload(DataClassDictMixin):
    """Payload for creating an endpoint group."""

    associated_endpoints: list[int] | None = Field(None, alias="associatedEndpoints")
    description: str | None = Field(None)
    name: str = Field(...)
    tag_i_ds: list[int] | None = Field(None, alias="tagIDs")


class EndpointGroupUpdatePayload(DataClassDictMixin):
    """Payload for updating an endpoint group."""

    description: str | None = Field(None)
    name: str | None = Field(None)
    tag_i_ds: list[int] | None = Field(None, alias="tagIDs")
    team_access_policies: portainer.TeamAccessPolicies | None = Field(None, alias="teamAccessPolicies")
    user_access_policies: portainer.UserAccessPolicies | None = Field(None, alias="userAccessPolicies")
