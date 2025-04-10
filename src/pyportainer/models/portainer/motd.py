"""Data models for Message of the Day (MOTD) in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class MotdResponse(DataClassDictMixin):
    """Response containing MOTD details."""

    content_layout: dict[str, str] | None = Field(None, alias="ContentLayout")
    hash: list[int] | None = Field(None, alias="Hash")
    message: str | None = Field(None, alias="Message")
    style: str | None = Field(None, alias="Style")
    title: str | None = Field(None, alias="Title")
