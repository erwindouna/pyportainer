"""Model for Docker container inspection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class HealthLog(DataClassORJSONMixin):
    """Represents a health log entry for a Docker container."""

    start: str | None = field(default=None, metadata=field_options(alias="Start"))
    end: str | None = field(default=None, metadata=field_options(alias="End"))
    exit_code: int | None = field(default=None, metadata=field_options(alias="ExitCode"))
    output: str | None = field(default=None, metadata=field_options(alias="Output"))


@dataclass
class Health(DataClassORJSONMixin):
    """Represents the health status of a Docker container."""

    status: str | None = field(default=None, metadata=field_options(alias="Status"))
    failing_streak: int | None = field(default=None, metadata=field_options(alias="FailingStreak"))
    log: list[HealthLog] | None = field(default=None, metadata=field_options(alias="Log"))


@dataclass
class State(DataClassORJSONMixin):
    """Represents the state of a Docker container."""

    status: str | None = field(default=None, metadata=field_options(alias="Status"))
    running: bool | None = field(default=None, metadata=field_options(alias="Running"))
    paused: bool | None = field(default=None, metadata=field_options(alias="Paused"))
    restarting: bool | None = field(default=None, metadata=field_options(alias="Restarting"))
    oom_killed: bool | None = field(default=None, metadata=field_options(alias="OOMKilled"))
    dead: bool | None = field(default=None, metadata=field_options(alias="Dead"))
    pid: int | None = field(default=None, metadata=field_options(alias="Pid"))
    exit_code: int | None = field(default=None, metadata=field_options(alias="ExitCode"))
    error: str | None = field(default=None, metadata=field_options(alias="Error"))
    started_at: str | None = field(default=None, metadata=field_options(alias="StartedAt"))
    finished_at: str | None = field(default=None, metadata=field_options(alias="FinishedAt"))
    health: Health | None = field(default=None, metadata=field_options(alias="Health"))


@dataclass
class ImageManifestDescriptorPlatform(DataClassORJSONMixin):
    """Represents the platform information of an image manifest descriptor."""

    architecture: str | None = None
    os: str | None = None
    variant: str | None = None
    os_version: str | None = field(default=None, metadata=field_options(alias="os.version"))
    os_features: list[str] | None = field(default=None, metadata=field_options(alias="os.features"))


@dataclass
class ImageManifestDescriptor(DataClassORJSONMixin):
    """Represents an image manifest descriptor."""

    media_type: str | None = field(default=None, metadata=field_options(alias="mediaType"))
    digest: str | None = None
    size: int | None = None
    urls: list[str] | None = None
    annotations: dict[str, str] | None = None
    data: Any | None = None
    platform: ImageManifestDescriptorPlatform | None = None
    artifact_type: Any | None = field(default=None, metadata=field_options(alias="artifactType"))


@dataclass
class GraphDriver(DataClassORJSONMixin):
    """Represents the graph driver information for a Docker container."""

    name: str | None = field(default=None, metadata=field_options(alias="Name"))
    data: dict[str, str] | None = field(default=None, metadata=field_options(alias="Data"))


@dataclass
class DockerInspect(DataClassORJSONMixin):
    """Represents the Docker container inspection data."""

    id: str | None = field(default=None, metadata=field_options(alias="Id"))
    created: str | None = field(default=None, metadata=field_options(alias="Created"))
    path: str | None = field(default=None, metadata=field_options(alias="Path"))
    args: list[str] | None = field(default=None, metadata=field_options(alias="Args"))
    state: State | None = field(default=None, metadata=field_options(alias="State"))
    image: str | None = field(default=None, metadata=field_options(alias="Image"))
    resolv_conf_path: str | None = field(default=None, metadata=field_options(alias="ResolvConfPath"))
    hostname_path: str | None = field(default=None, metadata=field_options(alias="HostnamePath"))
    hosts_path: str | None = field(default=None, metadata=field_options(alias="HostsPath"))
    log_path: str | None = field(default=None, metadata=field_options(alias="LogPath"))
    name: str | None = field(default=None, metadata=field_options(alias="Name"))
    restart_count: int | None = field(default=None, metadata=field_options(alias="RestartCount"))
    driver: str | None = field(default=None, metadata=field_options(alias="Driver"))
    platform: str | None = field(default=None, metadata=field_options(alias="Platform"))
    image_manifest_descriptor: ImageManifestDescriptor | None = field(default=None, metadata=field_options(alias="ImageManifestDescriptor"))
    mount_label: str | None = field(default=None, metadata=field_options(alias="MountLabel"))
    process_label: str | None = field(default=None, metadata=field_options(alias="ProcessLabel"))
    app_armor_profile: str | None = field(default=None, metadata=field_options(alias="AppArmorProfile"))
    exec_ids: list[str] | None = field(default=None, metadata=field_options(alias="ExecIDs"))
    graph_driver: GraphDriver | None = field(default=None, metadata=field_options(alias="GraphDriver"))
