"""Data models for edge jobs in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class EdgeJobCreateFromFileContentPayload(DataClassDictMixin):
    """Payload for creating an edge job from file content."""

    cron_expression: str | None = Field(None, alias="cronExpression")
    edge_groups: list[int] | None = Field(None, alias="edgeGroups")
    endpoints: list[int] | None = None
    file_content: str | None = Field(None, alias="fileContent")
    name: str | None = None
    recurring: bool | None = None


class EdgeJobFileResponse(DataClassDictMixin):
    """Response containing edge job file content."""

    file_content: str | None = Field(None, alias="FileContent")


class EdgeJobUpdatePayload(DataClassDictMixin):
    """Payload for updating an edge job."""

    cron_expression: str | None = Field(None, alias="cronExpression")
    edge_groups: list[int] | None = Field(None, alias="edgeGroups")
    endpoints: list[int] | None = None
    file_content: str | None = Field(None, alias="fileContent")
    name: str | None = None
    recurring: bool | None = None


class FileResponse(DataClassDictMixin):
    """Response containing file content."""

    file_content: str | None = Field(None, alias="FileContent")


class TaskContainer(DataClassDictMixin):
    """Represents a task container in an edge job."""

    endpoint_id: int | None = Field(None, alias="EndpointId")
    id: str | None = Field(None, alias="Id")
    logs_status: int | None = Field(None, alias="LogsStatus")
