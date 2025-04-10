"""Data models for GitOps operations in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class FileResponse(DataClassDictMixin):
    """Response containing file content."""

    file_content: str | None = Field(None, alias="fileContent")


class RepositoryFilePreviewPayload(DataClassDictMixin):
    """Payload for previewing a file in a Git repository."""

    password: str | None = Field(None)
    reference: str | None = Field(None)
    repository: str = Field(...)
    target_file: str | None = Field(None, alias="targetFile")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")
    username: str | None = Field(None)
