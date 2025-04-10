"""Data models for custom templates in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class FileResponse(DataClassDictMixin):
    """Response containing file content."""

    file_content: str | None = Field(None, alias="fileContent")


class CustomTemplateFromFileContentPayload(DataClassDictMixin):
    """Payload for creating a custom template from file content."""

    description: str = Field(...)
    edge_template: bool | None = Field(None, alias="edgeTemplate")
    file_content: str = Field(..., alias="fileContent")
    logo: str | None = Field(None)
    note: str | None = Field(None)
    platform: int | None = Field(None)
    title: str = Field(...)
    type: int = Field(...)
    variables: list[portainer.CustomTemplateVariableDefinition] | None = Field(None)


class CustomTemplateFromGitRepositoryPayload(DataClassDictMixin):
    """Payload for creating a custom template from a Git repository."""

    compose_file_path_in_repository: str | None = Field("docker-compose.yml", alias="composeFilePathInRepository")
    description: str = Field(...)
    edge_template: bool | None = Field(None, alias="edgeTemplate")
    is_compose_format: bool | None = Field(None, alias="isComposeFormat")
    logo: str | None = Field(None)
    note: str | None = Field(None)
    platform: int | None = Field(None)
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_url: str = Field(..., alias="repositoryURL")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    title: str = Field(...)
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")
    type: int = Field(...)
    variables: list[portainer.CustomTemplateVariableDefinition] | None = Field(None)


class CustomTemplateUpdatePayload(DataClassDictMixin):
    """Payload for updating a custom template."""

    compose_file_path_in_repository: str | None = Field("docker-compose.yml", alias="composeFilePathInRepository")
    description: str = Field(...)
    edge_template: bool | None = Field(None, alias="edgeTemplate")
    file_content: str = Field(..., alias="fileContent")
    is_compose_format: bool | None = Field(None, alias="isComposeFormat")
    logo: str | None = Field(None)
    note: str | None = Field(None)
    platform: int | None = Field(None)
    repository_authentication: bool | None = Field(None, alias="repositoryAuthentication")
    repository_git_credential_id: int | None = Field(None, alias="repositoryGitCredentialID")
    repository_password: str | None = Field(None, alias="repositoryPassword")
    repository_reference_name: str | None = Field(None, alias="repositoryReferenceName")
    repository_url: str = Field(..., alias="repositoryURL")
    repository_username: str | None = Field(None, alias="repositoryUsername")
    title: str = Field(...)
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")
    type: int = Field(...)
    variables: list[portainer.CustomTemplateVariableDefinition] | None = Field(None)


class CustomTemplatePayload(DataClassDictMixin):
    """Payload for creating a custom template."""

    template_id: int | None = Field(default=None, alias="templateID")
