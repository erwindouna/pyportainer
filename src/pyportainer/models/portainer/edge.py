"""Data models for edge-related operations in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import filesystem, portainer


class DeployerOptionsPayload(DataClassDictMixin):
    """Options for deploying edge stacks."""

    prune: bool | None = Field(None)
    remove_volumes: bool | None = Field(None, alias="removeVolumes")


class RegistryCredentials(DataClassDictMixin):
    """Credentials for accessing a Docker registry."""

    secret: str | None = None
    server_url: str | None = Field(None, alias="serverURL")
    username: str | None = None


class StackPayload(DataClassDictMixin):
    """Payload for managing edge stacks."""

    deployer_options_payload: DeployerOptionsPayload | None = Field(None, alias="deployerOptionsPayload")
    dir_entries: list[filesystem.DirEntry] | None = Field(None, alias="dirEntries")
    edge_update_id: int | None = Field(None, alias="edgeUpdateID")
    entry_file_name: str | None = Field(None, alias="entryFileName")
    env_vars: list[portainer.Pair] | None = Field(None, alias="envVars")
    filesystem_path: str | None = Field(None, alias="filesystemPath")
    id: int | None = None
    name: str | None = None
    namespace: str | None = None
    pre_pull_image: bool | None = Field(None, alias="prePullImage")
    re_pull_image: bool | None = Field(None, alias="rePullImage")
    ready_re_pull_image: bool | None = Field(None, alias="readyRePullImage")
    registry_credentials: list[RegistryCredentials] | None = Field(None, alias="registryCredentials")
    retry_deploy: bool | None = Field(None, alias="retryDeploy")
    retry_period: int | None = Field(None, alias="retryPeriod")
    rollback_to: int | None = Field(None, alias="rollbackTo")
    stack_file_content: str | None = Field(None, alias="stackFileContent")
    support_relative_path: bool | None = Field(None, alias="supportRelativePath")
    version: int | None = None


class EdgePayload(DataClassDictMixin):
    """Payload for edge-related operations."""

    edge_id: int | None = Field(default=None, alias="edgeID")
