"""Data models for edge groups in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class DecoratedEdgeGroup(DataClassDictMixin):
    """Represents a decorated edge group."""

    dynamic: bool | None = Field(None, alias="Dynamic")
    endpoints: list[int] | None = Field(None, alias="Endpoints")
    has_edge_job: bool | None = Field(None, alias="HasEdgeJob")
    has_edge_stack: bool | None = Field(None, alias="HasEdgeStack")
    id: int | None = Field(None, alias="Id")
    name: str | None = Field(None, alias="Name")
    partial_match: bool | None = Field(None, alias="PartialMatch")
    tag_ids: list[int] | None = Field(None, alias="TagIds")
    trusted_endpoints: list[int] | None = Field(None, alias="TrustedEndpoints")
    endpoint_types: list[int] | None = Field(None, alias="endpointTypes")


class EdgeGroupCreatePayload(DataClassDictMixin):
    """Payload for creating an edge group."""

    dynamic: bool | None = None
    endpoints: list[int] | None = None
    name: str | None = None
    partial_match: bool | None = Field(None, alias="partialMatch")
    tag_i_ds: list[int] | None = Field(None, alias="tagIDs")


class EdgeGroupUpdatePayload(DataClassDictMixin):
    """Payload for updating an edge group."""

    dynamic: bool | None = None
    endpoints: list[int] | None = None
    name: str | None = None
    partial_match: bool | None = Field(None, alias="partialMatch")
    tag_i_ds: list[int] | None = Field(None, alias="tagIDs")
