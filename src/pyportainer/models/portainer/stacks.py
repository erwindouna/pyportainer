"""Data models for stack management in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class ComposeStackFromFileContentPayload(DataClassDictMixin):
    """Payload for deploying a Compose stack from file content."""

    env: list[portainer.Pair] | None = Field(None)
    from_app_template: bool | None = Field(None, alias="fromAppTemplate")
    name: str = Field(...)
    stack_file_content: str = Field(..., alias="stackFileContent")


class ComposeStackFromGitRepositoryPayload(DataClassDictMixin):
    """Payload for deploying a Compose stack from a Git repository."""

    additional_files: list[str] | None = Field(None, alias="additionalFiles")
    auto_update: portainer.AutoUpdateSettings | None = Field(None, alias="autoUpdate")
    compose_file: str | None = Field("docker-compose.yml", alias="composeFile")
    env: list[portainer.Pair] | None = Field(None)
    from_app_template: bool | None = Field(None, alias="fromAppTemplate")
    name: str = Field(...)
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_url: str = Field(..., alias="repositoryURL")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")


class KubernetesGitDeploymentPayload(DataClassDictMixin):
    """Payload for deploying Kubernetes resources from a Git repository."""

    additional_files: list[str] | None = Field(None, alias="additionalFiles")
    auto_update: portainer.AutoUpdateSettings | None = Field(None, alias="autoUpdate")
    compose_format: bool | None = Field(None, alias="composeFormat")
    manifest_file: str | None = Field(None, alias="manifestFile")
    namespace: str | None = None
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_url: str | None = Field(None, alias="repositoryURL")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    stack_name: str | None = Field(None, alias="stackName")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")


class KubernetesManifestURLDeploymentPayload(DataClassDictMixin):
    """Payload for deploying Kubernetes resources from a manifest URL."""

    compose_format: bool | None = Field(None, alias="composeFormat")
    manifest_url: str | None = Field(None, alias="manifestURL")
    namespace: str | None = None
    stack_name: str | None = Field(None, alias="stackName")


class KubernetesStringDeploymentPayload(DataClassDictMixin):
    """Payload for deploying Kubernetes resources from a string manifest."""

    compose_format: bool | None = Field(None, alias="composeFormat")
    from_app_template: bool | None = Field(None, alias="fromAppTemplate")
    namespace: str | None = None
    stack_file_content: str | None = Field(None, alias="stackFileContent")
    stack_name: str | None = Field(None, alias="stackName")


class StackFileResponse(DataClassDictMixin):
    """Response containing the content of a stack file."""

    stack_file_content: str | None = Field(None, alias="StackFileContent")


class StackGitRedployPayload(DataClassDictMixin):
    """Payload for redeploying a stack from a Git repository."""

    env: list[portainer.Pair] | None = None
    prune: bool | None = None
    pull_image: bool | None = Field(None, alias="pullImage")
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    stack_name: str | None = Field(None, alias="stackName")


class StackGitUpdatePayload(DataClassDictMixin):
    """Payload for updating a stack from a Git repository."""

    auto_update: portainer.AutoUpdateSettings | None = Field(None, alias="autoUpdate")
    env: list[portainer.Pair] | None = None
    prune: bool | None = None
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")


class StackMigratePayload(DataClassDictMixin):
    """Payload for migrating a stack to another environment."""

    endpoint_id: int = Field(..., alias="endpointID")
    name: str | None = Field(None)
    swarm_id: str | None = Field(None, alias="swarmID")


class SwarmStackFromFileContentPayload(DataClassDictMixin):
    """Payload for deploying a Swarm stack from file content."""

    env: list[portainer.Pair] | None = Field(None)
    from_app_template: bool | None = Field(None, alias="fromAppTemplate")
    name: str = Field(...)
    stack_file_content: str = Field(..., alias="stackFileContent")
    swarm_id: str = Field(..., alias="swarmID")


class SwarmStackFromGitRepositoryPayload(DataClassDictMixin):
    """Payload for deploying a Swarm stack from a Git repository."""

    additional_files: list[str] | None = Field(None, alias="additionalFiles")
    auto_update: portainer.AutoUpdateSettings | None = Field(None, alias="autoUpdate")
    compose_file: str | None = Field("docker-compose.yml", alias="composeFile")
    env: list[portainer.Pair] | None = Field(None)
    from_app_template: bool | None = Field(None, alias="fromAppTemplate")
    name: str = Field(...)
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_url: str = Field(..., alias="repositoryURL")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    swarm_id: str = Field(..., alias="swarmID")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")


class UpdateSwarmStackPayload(DataClassDictMixin):
    """Payload for updating a Swarm stack."""

    env: list[portainer.Pair] | None = Field(None)
    prune: bool | None = Field(None)
    pull_image: bool | None = Field(None, alias="pullImage")
    stack_file_content: str | None = Field(None, alias="stackFileContent")
