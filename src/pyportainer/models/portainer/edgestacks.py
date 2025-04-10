"""Data models for edge stacks in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class EdgeStackFromGitRepositoryPayload(DataClassDictMixin):
    """Payload for creating an edge stack from a Git repository."""

    deployment_type: int | None = Field(None, alias="deploymentType")
    edge_groups: list[int] = Field(..., alias="edgeGroups")
    file_path_in_repository: str | None = Field("docker-compose.yml", alias="filePathInRepository")
    name: str = Field(...)
    registries: list[int] | None = Field(None)
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_url: str = Field(..., alias="repositoryURL")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")
    use_manifest_namespaces: bool | None = Field(None, alias="useManifestNamespaces")


class EdgeStackFromStringPayload(DataClassDictMixin):
    """Payload for creating an edge stack from a string."""

    deployment_type: int | None = Field(None, alias="deploymentType")
    edge_groups: list[int] | None = Field(None, alias="edgeGroups")
    name: str = Field(...)
    registries: list[int] | None = Field(None)
    stack_file_content: str = Field(..., alias="stackFileContent")
    use_manifest_namespaces: bool | None = Field(None, alias="useManifestNamespaces")


class StackFileResponse(DataClassDictMixin):
    """Response containing stack file content."""

    stack_file_content: str | None = Field(None, alias="StackFileContent")


class UpdateEdgeStackPayload(DataClassDictMixin):
    """Payload for updating an edge stack."""

    deployment_type: int | None = Field(None, alias="deploymentType")
    edge_groups: list[int] | None = Field(None, alias="edgeGroups")
    stack_file_content: str | None = Field(None, alias="stackFileContent")
    update_version: bool | None = Field(None, alias="updateVersion")
    use_manifest_namespaces: bool | None = Field(None, alias="useManifestNamespaces")


class UpdateStatusPayload(DataClassDictMixin):
    """Payload for updating the status of an edge stack."""

    endpoint_id: int | None = Field(None, alias="endpointID")
    error: str | None = None
    status: int | None = Field(None)
    time: int | None = None
    version: int | None = None
