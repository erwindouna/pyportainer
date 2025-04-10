"""Data models for integer or string types in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class IntOrString(DataClassDictMixin):
    """Represents a value that can be an integer or a string."""

    int_val: int | None = Field(None, alias="intVal")
    str_val: str | None = Field(None, alias="strVal")
    type: int | None = None
