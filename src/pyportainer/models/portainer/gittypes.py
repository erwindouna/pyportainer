"""Data models for Git-related types in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class GitAuthentication(DataClassDictMixin):
    """Represents Git authentication credentials."""

    git_credential_id: int | None = Field(None, alias="gitCredentialID")
    password: str | None = None
    username: str | None = None


class RepoConfig(DataClassDictMixin):
    """Configuration details for a Git repository."""

    authentication: GitAuthentication | None = None
    config_file_path: str | None = Field(None, alias="configFilePath")
    config_hash: str | None = Field(None, alias="configHash")
    reference_name: str | None = Field(None, alias="referenceName")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")
    url: str | None = Field(None)
