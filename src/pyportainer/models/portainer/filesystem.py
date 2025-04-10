"""Data models for filesystem operations in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class DirEntry(DataClassDictMixin):
    """Represents a directory entry in the filesystem."""

    content: str | None = None
    is_file: bool | None = Field(None, alias="isFile")
    name: str | None = None
    permissions: int | None = None
