"""Models for Docker events."""

from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class DockerEventActor(DataClassORJSONMixin):
    """Represents the actor of a Docker event."""

    id: str | None = field(default=None, metadata=field_options(alias="ID"))
    attributes: dict[str, str] | None = field(default=None, metadata=field_options(alias="Attributes"))


@dataclass
class DockerEvent(DataClassORJSONMixin):
    """Represents a Docker daemon event."""

    type: str | None = field(default=None, metadata=field_options(alias="Type"))
    action: str | None = field(default=None, metadata=field_options(alias="Action"))
    actor: DockerEventActor | None = field(default=None, metadata=field_options(alias="Actor"))
    scope: str | None = field(default=None, metadata=field_options(alias="scope"))
    time: int | None = field(default=None, metadata=field_options(alias="time"))
    time_nano: int | None = field(default=None, metadata=field_options(alias="timeNano"))
