"""Models for Docker API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class LocalImageInformation(DataClassORJSONMixin):  # pylint: disable=too-many-instance-attributes
    """Represents the local image information, from the Docker daemon."""

    id: str = field(metadata=field_options(alias="Id"))
    repo_tags: list[str] | None = field(default=None, metadata=field_options(alias="RepoTags"))
    repo_digests: list[str] | None = field(default=None, metadata=field_options(alias="RepoDigests"))
    parent: str | None = field(default=None, metadata=field_options(alias="Parent"))
    comment: str | None = field(default=None, metadata=field_options(alias="Comment"))
    created: str | None = field(default=None, metadata=field_options(alias="Created"))
    container: str | None = field(default=None, metadata=field_options(alias="Container"))
    container_config: dict[str, Any] | None = field(default=None, metadata=field_options(alias="ContainerConfig"))
    docker_version: str | None = field(default=None, metadata=field_options(alias="DockerVersion"))
    author: str | None = field(default=None, metadata=field_options(alias="Author"))
    config: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Config"))
    architecture: str | None = field(default=None, metadata=field_options(alias="Architecture"))
    variant: str | None = field(default=None, metadata=field_options(alias="Variant"))
    os: str | None = field(default=None, metadata=field_options(alias="Os"))
    os_version: str | None = field(default=None, metadata=field_options(alias="OsVersion"))
    size: int | None = field(default=None, metadata=field_options(alias="Size"))
    virtual_size: int | None = field(default=None, metadata=field_options(alias="VirtualSize"))
    graph_driver: dict[str, Any] | None = field(default=None, metadata=field_options(alias="GraphDriver"))
    root_fs: dict[str, Any] | None = field(default=None, metadata=field_options(alias="RootFS"))
    metadata: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Metadata"))
    labels: dict[str, str] | None = field(default=None, metadata=field_options(alias="Labels"))


@dataclass
class ImageInformation(DataClassORJSONMixin):
    """Represents the image information, from the registry."""

    descriptor: ImageManifestDescriptor | None = field(default=None, metadata=field_options(alias="Descriptor"))
    platforms: list[ImageManifestDescriptorPlatform] | None = field(default=None, metadata=field_options(alias="Platforms"))


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

    total_pgmajfault: int = field(default=0)
    cache: int = field(default=0)
    mapped_file: int = field(default=0)
    total_inactive_file: int = field(default=0)
    pgpgout: int = field(default=0)
    rss: int = field(default=0)
    total_mapped_file: int = field(default=0)
    writeback: int = field(default=0)
    unevictable: int = field(default=0)
    pgpgin: int = field(default=0)
    total_unevictable: int = field(default=0)
    pgmajfault: int = field(default=0)
    total_rss: int = field(default=0)
    total_rss_huge: int = field(default=0)
    total_writeback: int = field(default=0)
    total_inactive_anon: int = field(default=0)
    rss_huge: int = field(default=0)
    hierarchical_memory_limit: int = field(default=0)
    total_pgfault: int = field(default=0)
    total_active_file: int = field(default=0)
    active_anon: int = field(default=0)
    total_active_anon: int = field(default=0)
    total_pgpgout: int = field(default=0)
    total_cache: int = field(default=0)
    inactive_anon: int = field(default=0)
    active_file: int = field(default=0)
    pgfault: int = field(default=0)
    inactive_file: int = field(default=0)
    total_pgpgin: int = field(default=0)


@dataclass
class MemoryStats(DataClassORJSONMixin):
    """Represents memory statistics for a Docker container."""

    stats: MemoryStatsDetails = field(default_factory=MemoryStatsDetails)
    max_usage: int = field(default=0)
    usage: int = field(default=0)
    failcnt: int = field(default=0)
    limit: int = field(default=0)


@dataclass
class ThrottlingData(DataClassORJSONMixin):
    """Represents CPU throttling data for a Docker container."""

    periods: int = field(default=0)
    throttled_periods: int = field(default=0)
    throttled_time: int = field(default=0)


@dataclass
class CpuUsage(DataClassORJSONMixin):
    """Represents CPU usage statistics for a Docker container."""

    total_usage: int = field(default=0)
    usage_in_kernelmode: int = field(default=0)
    usage_in_usermode: int = field(default=0)
    percpu_usage: list[int] = field(default_factory=list)


@dataclass
class CpuStats(DataClassORJSONMixin):
    """Represents CPU statistics for a Docker container."""

    cpu_usage: CpuUsage = field(default_factory=CpuUsage)
    system_cpu_usage: int = field(default=0)
    online_cpus: int = field(default=0)
    throttling_data: ThrottlingData = field(default_factory=ThrottlingData)


@dataclass
class DockerContainerStats(DataClassORJSONMixin):
    """Represents Docker container statistics."""

    read: str = field(default="")
    preread: str = field(default="")
    pids_stats: PidsStats = field(default_factory=PidsStats)
    networks: dict[str, NetworkStats] = field(default_factory=dict)
    memory_stats: MemoryStats = field(default_factory=MemoryStats)
    blkio_stats: dict[str, Any] = field(default_factory=dict)
    cpu_stats: CpuStats = field(default_factory=CpuStats)
    precpu_stats: CpuStats | None = field(default_factory=CpuStats)
