"""Models for Docker API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


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

    digest: str | None = None
    size: int | None = None
    urls: list[str] | None = None
    annotations: dict[str, str] | None = None
    data: Any | None = None
    platform: ImageManifestDescriptorPlatform | None = None
    media_type: str | None = field(default=None, metadata=field_options(alias="mediaType"))
    artifact_type: Any | None = field(default=None, metadata=field_options(alias="artifactType"))


@dataclass
class Port(DataClassORJSONMixin):
    """Represents a port mapping for a Docker container."""

    private_port: int | None = field(default=None, metadata=field_options(alias="PrivatePort"))
    public_port: int | None = field(default=None, metadata=field_options(alias="PublicPort"))
    type: str | None = field(default=None, metadata=field_options(alias="Type"))


@dataclass
class HostConfig(DataClassORJSONMixin):
    """Represents the host configuration for a Docker container."""

    annotations: dict[str, str] | None = None
    network_mode: str | None = field(default=None, metadata=field_options(alias="NetworkMode"))


@dataclass
class IPAMConfig(DataClassORJSONMixin):
    """Represents the IP Address Management (IPAM) configuration for a Docker container."""

    ipv4_address: str | None = field(default=None, metadata=field_options(alias="IPv4Address"))
    ipv6_address: str | None = field(default=None, metadata=field_options(alias="IPv6Address"))
    link_local_ips: list[str] | None = field(default=None, metadata=field_options(alias="LinkLocalIPs"))


@dataclass
class Network(DataClassORJSONMixin):
    """Represents the network configuration for a Docker container."""

    endpoint_id: str = field(metadata=field_options(alias="EndpointID"))

    links: list[str] | None = field(default=None, metadata=field_options(alias="Links"))
    aliases: list[str] | None = field(default=None, metadata=field_options(alias="Aliases"))
    gateway: str | None = field(default=None, metadata=field_options(alias="Gateway"))
    ipam_config: IPAMConfig | None = field(default=None, metadata=field_options(alias="IPAMConfig"))
    mac_address: str | None = field(default=None, metadata=field_options(alias="MacAddress"))
    driver_opts: dict[str, str] | None = field(default=None, metadata=field_options(alias="DriverOpts"))
    network_id: str | None = field(default=None, metadata=field_options(alias="NetworkID"))
    ip_address: str | None = field(default=None, metadata=field_options(alias="IPAddress"))
    ip_prefix_len: int | None = field(default=None, metadata=field_options(alias="IPPrefixLen"))
    ipv6_gateway: str | None = field(default=None, metadata=field_options(alias="IPv6Gateway"))
    global_ipv6_address: str | None = field(default=None, metadata=field_options(alias="GlobalIPv6Address"))
    global_ipv6_prefix_len: int | None = field(default=None, metadata=field_options(alias="GlobalIPv6PrefixLen"))
    dns_names: list[str] | None = field(default=None, metadata=field_options(alias="DNSNames"))


@dataclass
class NetworkSettings(DataClassORJSONMixin):
    """Represents the network settings for a Docker container."""

    networks: dict[str, Network] | None = field(default=None, metadata=field_options(alias="Networks"))


@dataclass
class Mount(DataClassORJSONMixin):
    """Represents a mount point for a Docker container."""

    type: str | None = field(default=None, metadata=field_options(alias="Type"))
    name: str | None = field(default=None, metadata=field_options(alias="Name"))
    source: str | None = field(default=None, metadata=field_options(alias="Source"))
    destination: str | None = field(default=None, metadata=field_options(alias="Destination"))
    driver: str | None = field(default=None, metadata=field_options(alias="Driver"))
    mode: str | None = field(default=None, metadata=field_options(alias="Mode"))
    rw: bool | None = field(default=None, metadata=field_options(alias="RW"))
    propagation: str | None = field(default=None, metadata=field_options(alias="Propagation"))


@dataclass
class DockerContainer(DataClassORJSONMixin):
    """Represents a Docker container."""

    id: str = field(metadata=field_options(alias="Id"))
    names: list[str] = field(default_factory=list, metadata=field_options(alias="Names"))

    image: str | None = field(default=None, metadata=field_options(alias="Image"))
    command: str | None = field(default=None, metadata=field_options(alias="Command"))
    created: str | None = field(default=None, metadata=field_options(alias="Created"))
    ports: list[Port] | None = field(default=None, metadata=field_options(alias="Ports"))
    labels: dict[str, str] | None = field(default=None, metadata=field_options(alias="Labels"))
    state: str | None = field(default=None, metadata=field_options(alias="State"))
    status: str | None = field(default=None, metadata=field_options(alias="Status"))
    mounts: list[Mount] | None = field(default=None, metadata=field_options(alias="Mounts"))

    image_id: str | None = field(default=None, metadata=field_options(alias="ImageID"))
    image_manifest_descriptor: ImageManifestDescriptor | None = field(default=None, metadata=field_options(alias="ImageManifestDescriptor"))
    size_rw: str | None = field(default=None, metadata=field_options(alias="SizeRw"))
    size_root_fs: str | None = field(default=None, metadata=field_options(alias="SizeRootFs"))
    host_config: HostConfig | None = field(default=None, metadata=field_options(alias="HostConfig"))
    network_settings: NetworkSettings | None = field(default=None, metadata=field_options(alias="NetworkSettings"))


@dataclass
class PidsStats(DataClassORJSONMixin):
    """Represents PID statistics for a Docker container."""

    current: int | None = None


@dataclass
class NetworkStats(DataClassORJSONMixin):
    """Represents network statistics for a Docker container interface."""

    rx_bytes: int | None = None
    rx_dropped: int | None = None
    rx_errors: int | None = None
    rx_packets: int | None = None
    tx_bytes: int | None = None
    tx_dropped: int | None = None
    tx_errors: int | None = None
    tx_packets: int | None = None


@dataclass
class MemoryStatsDetails(DataClassORJSONMixin):  # pylint: disable=too-many-instance-attributes
    """Represents detailed memory statistics for a Docker container."""

    total_pgmajfault: int | None = None
    cache: int | None = None
    mapped_file: int | None = None
    total_inactive_file: int | None = None
    pgpgout: int | None = None
    rss: int | None = None
    total_mapped_file: int | None = None
    writeback: int | None = None
    unevictable: int | None = None
    pgpgin: int | None = None
    total_unevictable: int | None = None
    pgmajfault: int | None = None
    total_rss: int | None = None
    total_rss_huge: int | None = None
    total_writeback: int | None = None
    total_inactive_anon: int | None = None
    rss_huge: int | None = None
    hierarchical_memory_limit: int | None = None
    total_pgfault: int | None = None
    total_active_file: int | None = None
    active_anon: int | None = None
    total_active_anon: int | None = None
    total_pgpgout: int | None = None
    total_cache: int | None = None
    inactive_anon: int | None = None
    active_file: int | None = None
    pgfault: int | None = None
    inactive_file: int | None = None
    total_pgpgin: int | None = None


@dataclass
class MemoryStats(DataClassORJSONMixin):
    """Represents memory statistics for a Docker container."""

    stats: MemoryStatsDetails | None = None
    max_usage: int | None = None
    usage: int | None = None
    failcnt: int | None = None
    limit: int | None = None


@dataclass
class ThrottlingData(DataClassORJSONMixin):
    """Represents CPU throttling data for a Docker container."""

    periods: int | None = None
    throttled_periods: int | None = None
    throttled_time: int | None = None


@dataclass
class CpuUsage(DataClassORJSONMixin):
    """Represents CPU usage statistics for a Docker container."""

    percpu_usage: list[int]
    usage_in_usermode: int
    total_usage: int
    usage_in_kernelmode: int


@dataclass
class CpuStats(DataClassORJSONMixin):
    """Represents CPU statistics for a Docker container."""

    cpu_usage: CpuUsage
    system_cpu_usage: int
    online_cpus: int
    throttling_data: ThrottlingData


@dataclass
class DockerContainerStats(DataClassORJSONMixin):
    """Represents Docker container statistics."""

    memory_stats: MemoryStats
    blkio_stats: dict[str, Any]
    cpu_stats: CpuStats
    precpu_stats: CpuStats

    read: str | None = None
    preread: str | None = None
    pids_stats: PidsStats | None = None
    networks: dict[str, NetworkStats] | None = None
