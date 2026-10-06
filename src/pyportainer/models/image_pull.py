"""Models for Docker image pulls."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class DockerImagePullProgressDetail(DataClassORJSONMixin):
    """Represents the byte progress of a layer in an image pull."""

    current: int | None = None
    total: int | None = None


@dataclass
class DockerImagePullEvent(DataClassORJSONMixin):
    """Represents one line of the Docker image pull stream."""

    status: str | None = None
    id: str | None = None
    progress_detail: DockerImagePullProgressDetail | None = field(default=None, metadata=field_options(alias="progressDetail"))
    error: str | None = None
