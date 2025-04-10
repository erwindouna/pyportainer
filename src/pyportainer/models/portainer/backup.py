"""Data models for backup and restore operations."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class BackupPayload(DataClassDictMixin):
    """Payload for creating a backup."""

    password: str | None = None


class RestorePayload(DataClassDictMixin):
    """Payload for restoring from a backup."""

    file_content: list[int] | None = Field(None, alias="fileContent")
    file_name: str | None = Field(None, alias="fileName")
    password: str | None = None
