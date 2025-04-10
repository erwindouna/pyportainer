"""Data models for system-related operations in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import build as build_1


class NodesCountResponse(DataClassDictMixin):
    """Response containing the count of nodes."""

    nodes: int | None = None


class Status(DataClassDictMixin):
    """Represents the status of the Portainer API."""

    version: str | None = Field(None, alias="Version")
    instance_id: str | None = Field(None, alias="instanceID")


class SystemInfoResponse(DataClassDictMixin):
    """Response containing system information."""

    agents: int | None = None
    edge_agents: int | None = Field(None, alias="edgeAgents")
    platform: str | None = None


class VersionResponse(DataClassDictMixin):
    """Response containing version information."""

    latest_version: str | None = Field(None, alias="LatestVersion")
    server_edition: str | None = Field(None, alias="ServerEdition")
    update_available: bool | None = Field(None, alias="UpdateAvailable")
    version_support: str | None = Field(None, alias="VersionSupport")
    build: build_1.BuildInfo | None = None
    database_version: str | None = Field(None, alias="databaseVersion")
    dependencies: build_1.DependenciesInfo | None = None
    runtime: build_1.RuntimeInfo | None = None
    server_version: str | None = Field(None, alias="serverVersion")


class SystemInfo(DataClassDictMixin):
    """Represents system information."""

    version: str | None = None
    uptime: int | None = None
    cpu_count: int | None = Field(None, alias="cpuCount")
