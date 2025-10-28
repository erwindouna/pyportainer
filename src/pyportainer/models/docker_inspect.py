"""Model for Docker container inspection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import SerializationStrategy


# Custom serialization strategy for Optional[int] fields that may be empty string
class OptionalIntStringNoneStrategy(SerializationStrategy):
    """Custom strategy to handle Optional[int] fields that may be empty strings."""

    def deserialize(self, value: Any) -> Any:
        """Deserialize value to Optional[int], treating empty strings as None."""
        if value == "" or value is None:
            return None
        return int(value)

    def serialize(self, value: Any) -> Any:
        """Serialize Optional[int] value."""
        return value


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
class DockerInspectConfig(DataClassORJSONMixin):  # pylint: disable=too-many-instance-attributes
    """Represents the configuration of a Docker container."""

    hostname: str | None = field(default=None, metadata=field_options(alias="Hostname"))
    domainname: str | None = field(default=None, metadata=field_options(alias="Domainname"))
    user: str | None = field(default=None, metadata=field_options(alias="User"))
    attach_stdin: bool | None = field(default=None, metadata=field_options(alias="AttachStdin"))
    attach_stdout: bool | None = field(default=None, metadata=field_options(alias="AttachStdout"))
    attach_stderr: bool | None = field(default=None, metadata=field_options(alias="AttachStderr"))
    tty: bool | None = field(default=None, metadata=field_options(alias="Tty"))
    open_stdin: bool | None = field(default=None, metadata=field_options(alias="OpenStdin"))
    stdin_once: bool | None = field(default=None, metadata=field_options(alias="StdinOnce"))
    env: list[str] | None = field(default=None, metadata=field_options(alias="Env"))
    cmd: list[str] | None = field(default=None, metadata=field_options(alias="Cmd"))
    image: str | None = field(default=None, metadata=field_options(alias="Image"))
    working_dir: str | None = field(default=None, metadata=field_options(alias="WorkingDir"))
    entrypoint: list[str] | None = field(default=None, metadata=field_options(alias="Entrypoint"))
    labels: dict[str, str] | None = field(default=None, metadata=field_options(alias="Labels"))
    healthcheck: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Healthcheck"))
    mac_address: str | None = field(default=None, metadata=field_options(alias="MacAddress"))
    network_disabled: bool | None = field(default=None, metadata=field_options(alias="NetworkDisabled"))
    volumes: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Volumes"))
    stop_signal: str | None = field(default=None, metadata=field_options(alias="StopSignal"))
    stop_timeout: int | None = field(default=None, metadata=field_options(alias="StopTimeout"))


@dataclass
class DockerInspectHostConfig(DataClassORJSONMixin):  # pylint: disable=too-many-instance-attributes
    """Represents the host configuration of a Docker container."""

    maximum_iops: int | None = field(default=None, metadata=field_options(alias="MaximumIOps"))
    maximum_iobps: int | None = field(default=None, metadata=field_options(alias="MaximumIOBps"))
    blkio_weight: int | None = field(default=None, metadata=field_options(alias="BlkioWeight"))
    blkio_weight_device: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="BlkioWeightDevice"))
    blkio_device_read_bps: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="BlkioDeviceReadBps"))
    blkio_device_write_bps: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="BlkioDeviceWriteBps"))
    blkio_device_read_iops: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="BlkioDeviceReadIOps"))
    blkio_device_write_iops: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="BlkioDeviceWriteIOps"))
    container_id_file: str | None = field(default=None, metadata=field_options(alias="ContainerIDFile"))
    cpuset_cpus: str | None = field(default=None, metadata=field_options(alias="CpusetCpus"))
    cpuset_mems: str | None = field(default=None, metadata=field_options(alias="CpusetMems"))
    cpu_percent: int | None = field(default=None, metadata=field_options(alias="CpuPercent"))
    network_mode: str | None = field(default=None, metadata=field_options(alias="NetworkMode"))
    port_bindings: dict[str, list[dict[str, Any]]] | None = field(default=None, metadata=field_options(alias="PortBindings"))
    binds: list[str] | None = field(default=None, metadata=field_options(alias="Binds"))
    restart_policy: dict[str, Any] | None = field(default=None, metadata=field_options(alias="RestartPolicy"))
    cpu_shares: int | None = field(default=None, metadata=field_options(alias="CpuShares"))
    cpu_period: int | None = field(default=None, metadata=field_options(alias="CpuPeriod"))
    cpu_realtime_period: int | None = field(default=None, metadata=field_options(alias="CpuRealtimePeriod"))
    cpu_realtime_runtime: int | None = field(default=None, metadata=field_options(alias="CpuRealtimeRuntime"))
    memory: int | None = field(default=None, metadata=field_options(alias="Memory"))
    memory_swap: int | None = field(default=None, metadata=field_options(alias="MemorySwap"))
    memory_reservation: int | None = field(default=None, metadata=field_options(alias="MemoryReservation"))
    cgroup_parent: str | None = field(default=None, metadata=field_options(alias="CgroupParent"))
    devices: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="Devices"))
    device_requests: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="DeviceRequests"))
    ipc_mode: str | None = field(default=None, metadata=field_options(alias="IpcMode"))
    dns: list[str] | None = field(default=None, metadata=field_options(alias="Dns"))
    dns_search: list[str] | None = field(default=None, metadata=field_options(alias="DnsSearch"))
    oom_kill_disable: bool | None = field(default=None, metadata=field_options(alias="OomKillDisable"))
    oom_score_adj: int | None = field(default=None, metadata=field_options(alias="OomScoreAdj"))
    privileged: bool | None = field(default=None, metadata=field_options(alias="Privileged"))
    pid_mode: str | None = field(default=None, metadata=field_options(alias="PidMode"))
    volume_driver: str | None = field(default=None, metadata=field_options(alias="VolumeDriver"))
    readonly_rootfs: bool | None = field(default=None, metadata=field_options(alias="ReadonlyRootfs"))
    publish_all_ports: bool | None = field(default=None, metadata=field_options(alias="PublishAllPorts"))
    log_config: dict[str, Any] | None = field(default=None, metadata=field_options(alias="LogConfig"))
    sysctls: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Sysctls"))
    ulimits: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="Ulimits"))
    shm_size: int | None = field(default=None, metadata=field_options(alias="ShmSize"))


@dataclass
class DockerInspectNetworkSettings(DataClassORJSONMixin):
    """Represents the network settings of a Docker container."""

    bridge: str | None = field(default=None, metadata=field_options(alias="Bridge"))
    sandbox_id: str | None = field(default=None, metadata=field_options(alias="SandboxID"))
    hairpin_mode: bool | None = field(default=None, metadata=field_options(alias="HairpinMode"))
    link_local_ipv6_address: str | None = field(default=None, metadata=field_options(alias="LinkLocalIPv6Address"))
    sandbox_key: str | None = field(default=None, metadata=field_options(alias="SandboxKey"))
    endpoint_id: str | None = field(default=None, metadata=field_options(alias="EndpointID"))
    gateway: str | None = field(default=None, metadata=field_options(alias="Gateway"))
    global_ipv6_address: str | None = field(default=None, metadata=field_options(alias="GlobalIPv6Address"))
    ip_address: str | None = field(default=None, metadata=field_options(alias="IPAddress"))
    ipv6_gateway: str | None = field(default=None, metadata=field_options(alias="IPv6Gateway"))
    mac_address: str | None = field(default=None, metadata=field_options(alias="MacAddress"))
    networks: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Networks"))


@dataclass
class GraphDriver(DataClassORJSONMixin):
    """Represents the graph driver information for a Docker container."""

    name: str | None = field(default=None, metadata=field_options(alias="Name"))
    data: dict[str, str] | None = field(default=None, metadata=field_options(alias="Data"))


@dataclass
class DockerInspect(DataClassORJSONMixin):  # pylint: disable=too-many-instance-attributes
    """Represents the Docker container inspection data."""

    @classmethod
    def preprocessor(cls, d: dict[str, Any]) -> dict[str, Any]:
        """Preprocess the Docker inspect payload to clean up certain fields."""
        ns = d.get("NetworkSettings")
        int_fields = ["LinkLocalIPv6PrefixLen", "GlobalIPv6PrefixLen", "IPPrefixLen"]
        if ns and isinstance(ns, dict):
            for int_field in int_fields:
                if int_field in ns and ns[int_field] == "":
                    ns[int_field] = None
        return d

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
    config: DockerInspectConfig | None = field(default=None, metadata=field_options(alias="Config"))
    host_config: DockerInspectHostConfig | None = field(default=None, metadata=field_options(alias="HostConfig"))
    network_settings: DockerInspectNetworkSettings | None = field(default=None, metadata=field_options(alias="NetworkSettings"))
    mounts: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="Mounts"))


@dataclass
class DockerVersion(DataClassORJSONMixin):
    """Represents the Docker version information."""

    @dataclass
    class PlatformInfo(DataClassORJSONMixin):
        """Represents the platform information for Docker version."""

        name: str | None = field(default=None, metadata=field_options(alias="Name"))

    platform: PlatformInfo | None = field(default=None, metadata=field_options(alias="Platform"))

    version: str | None = field(default=None, metadata=field_options(alias="Version"))
    api_version: str | None = field(default=None, metadata=field_options(alias="ApiVersion"))
    min_api_version: str | None = field(default=None, metadata=field_options(alias="MinAPIVersion"))
    git_commit: str | None = field(default=None, metadata=field_options(alias="GitCommit"))
    go_version: str | None = field(default=None, metadata=field_options(alias="GoVersion"))
    os: str | None = field(default=None, metadata=field_options(alias="Os"))
    arch: str | None = field(default=None, metadata=field_options(alias="Arch"))
    kernel_version: str | None = field(default=None, metadata=field_options(alias="KernelVersion"))
    build_time: str | None = field(default=None, metadata=field_options(alias="BuildTime"))
    experimental: bool | None = field(default=None, metadata=field_options(alias="Experimental"))
    components: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="Components"))
    warnings: list[str] | None = field(default=None, metadata=field_options(alias="Warnings"))


@dataclass
class CommitInfo(DataClassORJSONMixin):
    """Represents commit information for Docker components."""

    id: str | None = field(default=None, metadata=field_options(alias="ID"))
    expected: str | None = field(default=None, metadata=field_options(alias="Expected"))


@dataclass
class SwarmInfo(DataClassORJSONMixin):
    """Represents the Swarm mode information for a Docker daemon."""

    node_id: str | None = field(default=None, metadata=field_options(alias="NodeID"))
    node_addr: str | None = field(default=None, metadata=field_options(alias="NodeAddr"))
    local_node_state: str | None = field(default=None, metadata=field_options(alias="LocalNodeState"))
    control_available: bool | None = field(default=None, metadata=field_options(alias="ControlAvailable"))
    error: str | None = field(default=None, metadata=field_options(alias="Error"))
    remote_managers: list[Any] | None = field(default=None, metadata=field_options(alias="RemoteManagers"))
    nodes: int | None = field(default=None, metadata=field_options(alias="Nodes"))
    managers: int | None = field(default=None, metadata=field_options(alias="Managers"))
    cluster: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Cluster"))


@dataclass
class RegistryConfig(DataClassORJSONMixin):
    """Represents the registry configuration for a Docker daemon."""

    allow_nondistributable_artifacts_cidrs: list[str] | None = field(
        default=None, metadata=field_options(alias="AllowNondistributableArtifactsCIDRs")
    )
    allow_nondistributable_artifacts_hostnames: list[str] | None = field(
        default=None, metadata=field_options(alias="AllowNondistributableArtifactsHostnames")
    )
    insecure_registry_cidrs: list[str] | None = field(default=None, metadata=field_options(alias="InsecureRegistryCIDRs"))
    index_configs: dict[str, Any] | None = field(default=None, metadata=field_options(alias="IndexConfigs"))
    mirrors: list[str] | None = field(default=None, metadata=field_options(alias="Mirrors"))


@dataclass
class PluginsInfo(DataClassORJSONMixin):
    """Represents the plugins information for a Docker daemon."""

    volume: list[str] | None = field(default=None, metadata=field_options(alias="Volume"))
    network: list[str] | None = field(default=None, metadata=field_options(alias="Network"))
    authorization: list[str] | None = field(default=None, metadata=field_options(alias="Authorization"))
    log: list[str] | None = field(default=None, metadata=field_options(alias="Log"))


@dataclass
class DockerInfo(DataClassORJSONMixin):  # pylint: disable=too-many-instance-attributes
    """Represents the Docker daemon information."""

    id: str | None = field(default=None, metadata=field_options(alias="ID"))
    containers: int | None = field(default=None, metadata=field_options(alias="Containers"))
    containers_running: int | None = field(default=None, metadata=field_options(alias="ContainersRunning"))
    containers_paused: int | None = field(default=None, metadata=field_options(alias="ContainersPaused"))
    containers_stopped: int | None = field(default=None, metadata=field_options(alias="ContainersStopped"))
    images: int | None = field(default=None, metadata=field_options(alias="Images"))
    driver: str | None = field(default=None, metadata=field_options(alias="Driver"))
    driver_status: list[list[str]] | None = field(default=None, metadata=field_options(alias="DriverStatus"))
    docker_root_dir: str | None = field(default=None, metadata=field_options(alias="DockerRootDir"))
    plugins: PluginsInfo | None = field(default=None, metadata=field_options(alias="Plugins"))
    memory_limit: bool | None = field(default=None, metadata=field_options(alias="MemoryLimit"))
    swap_limit: bool | None = field(default=None, metadata=field_options(alias="SwapLimit"))
    kernel_memory_tcp: bool | None = field(default=None, metadata=field_options(alias="KernelMemoryTCP"))
    cpu_cfs_period: bool | None = field(default=None, metadata=field_options(alias="CpuCfsPeriod"))
    cpu_cfs_quota: bool | None = field(default=None, metadata=field_options(alias="CpuCfsQuota"))
    cpu_shares: bool | None = field(default=None, metadata=field_options(alias="CPUShares"))
    cpu_set: bool | None = field(default=None, metadata=field_options(alias="CPUSet"))
    pids_limit: bool | None = field(default=None, metadata=field_options(alias="PidsLimit"))
    oom_kill_disable: bool | None = field(default=None, metadata=field_options(alias="OomKillDisable"))
    ipv4_forwarding: bool | None = field(default=None, metadata=field_options(alias="IPv4Forwarding"))
    bridge_nf_iptables: bool | None = field(default=None, metadata=field_options(alias="BridgeNfIptables"))
    bridge_nf_ip6tables: bool | None = field(default=None, metadata=field_options(alias="BridgeNfIp6tables"))
    debug: bool | None = field(default=None, metadata=field_options(alias="Debug"))
    nfd: int | None = field(default=None, metadata=field_options(alias="NFd"))
    ngoroutines: int | None = field(default=None, metadata=field_options(alias="NGoroutines"))
    system_time: str | None = field(default=None, metadata=field_options(alias="SystemTime"))
    logging_driver: str | None = field(default=None, metadata=field_options(alias="LoggingDriver"))
    cgroup_driver: str | None = field(default=None, metadata=field_options(alias="CgroupDriver"))
    cgroup_version: str | None = field(default=None, metadata=field_options(alias="CgroupVersion"))
    nevents_listener: int | None = field(default=None, metadata=field_options(alias="NEventsListener"))
    kernel_version: str | None = field(default=None, metadata=field_options(alias="KernelVersion"))
    operating_system: str | None = field(default=None, metadata=field_options(alias="OperatingSystem"))
    os_version: str | None = field(default=None, metadata=field_options(alias="OSVersion"))
    os_type: str | None = field(default=None, metadata=field_options(alias="OSType"))
    architecture: str | None = field(default=None, metadata=field_options(alias="Architecture"))
    ncpu: int | None = field(default=None, metadata=field_options(alias="NCPU"))
    mem_total: int | None = field(default=None, metadata=field_options(alias="MemTotal"))
    index_server_address: str | None = field(default=None, metadata=field_options(alias="IndexServerAddress"))
    registry_config: RegistryConfig | None = field(default=None, metadata=field_options(alias="RegistryConfig"))
    generic_resources: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="GenericResources"))
    http_proxy: str | None = field(default=None, metadata=field_options(alias="HttpProxy"))
    https_proxy: str | None = field(default=None, metadata=field_options(alias="HttpsProxy"))
    no_proxy: str | None = field(default=None, metadata=field_options(alias="NoProxy"))
    name: str | None = field(default=None, metadata=field_options(alias="Name"))
    labels: list[str] | None = field(default=None, metadata=field_options(alias="Labels"))
    experimental_build: bool | None = field(default=None, metadata=field_options(alias="ExperimentalBuild"))
    server_version: str | None = field(default=None, metadata=field_options(alias="ServerVersion"))
    runtimes: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Runtimes"))
    default_runtime: str | None = field(default=None, metadata=field_options(alias="DefaultRuntime"))
    swarm: SwarmInfo | None = field(default=None, metadata=field_options(alias="Swarm"))
    live_restore_enabled: bool | None = field(default=None, metadata=field_options(alias="LiveRestoreEnabled"))
    isolation: str | None = field(default=None, metadata=field_options(alias="Isolation"))
    init_binary: str | None = field(default=None, metadata=field_options(alias="InitBinary"))
    containerd_commit: CommitInfo | None = field(default=None, metadata=field_options(alias="ContainerdCommit"))
    runc_commit: CommitInfo | None = field(default=None, metadata=field_options(alias="RuncCommit"))
    init_commit: CommitInfo | None = field(default=None, metadata=field_options(alias="InitCommit"))
    security_options: list[str] | None = field(default=None, metadata=field_options(alias="SecurityOptions"))
    product_license: str | None = field(default=None, metadata=field_options(alias="ProductLicense"))
    default_address_pools: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="DefaultAddressPools"))
    warnings: list[str] | None = field(default=None, metadata=field_options(alias="Warnings"))
