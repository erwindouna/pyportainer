"""Data models for endpoint edge operations in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class EdgeJobResponse(DataClassDictMixin):
    """Response containing details of an edge job."""

    collect_logs: bool | None = Field(None, alias="CollectLogs")
    cron_expression: str | None = Field(None, alias="CronExpression")
    id: int | None = Field(None, alias="Id")
    script: str | None = Field(None, alias="Script")
    version: int | None = Field(None, alias="Version")


class StackStatusResponse(DataClassDictMixin):
    """Response containing the status of an edge stack."""

    id: int | None = Field(None)
    version: int | None = Field(None)


class EndpointEdgeStatusInspectResponse(DataClassDictMixin):
    """Response containing the status of an endpoint edge."""

    checkin: int | None = Field(None)
    credentials: str | None = None
    port: int | None = Field(None)
    schedules: list[EdgeJobResponse] | None = Field(None)
    stacks: list[StackStatusResponse] | None = Field(None)
    status: str | None = Field(None)
