"""Data models for template management in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class FileResponse(DataClassDictMixin):
    """Response containing the content of a file."""

    file_content: str | None = Field(None, alias="fileContent")


class ListResponse(DataClassDictMixin):
    """Response containing a list of templates."""

    templates: list[portainer.Template] | None = None
    version: str | None = None
