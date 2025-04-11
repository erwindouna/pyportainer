"""Models for Portainer API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class KubernetesSnapshot(DataClassORJSONMixin):
    """Represents a Kubernetes snapshot, including diagnostics data, version, node count, and resource usage."""

    diagnostics_data: dict[str, str] | None = field(default=None, metadata=field_options(alias="DiagnosticsData"))
    kubernetes_version: str | None = field(default=None, metadata=field_options(alias="KubernetesVersion"))
    node_count: int | None = field(default=None, metadata=field_options(alias="NodeCount"))
    time: int | None = field(default=None, metadata=field_options(alias="Time"))
    total_cpu: int | None = field(default=None, metadata=field_options(alias="TotalCPU"))
    total_memory: int | None = field(default=None, metadata=field_options(alias="TotalMemory"))


@dataclass
class TLSConfig(DataClassORJSONMixin):
    """Represents TLS configuration."""

    tls: bool | None = field(default=None, metadata=field_options(alias="TLS"))
    tls_ca_cert: str | None = field(default=None, metadata=field_options(alias="TLSCACert"))
    tls_cert: str | None = field(default=None, metadata=field_options(alias="TLSCert"))
    tls_key: str | None = field(default=None, metadata=field_options(alias="TLSKey"))
    tls_skip_verify: bool | None = field(default=None, metadata=field_options(alias="TLSSkipVerify"))


@dataclass
class SecuritySettings(DataClassORJSONMixin):
    """Represents security settings for an endpoint."""

    allow_bind_mounts_for_regular_users: bool | None = field(default=None, metadata=field_options(alias="allowBindMountsForRegularUsers"))
    allow_container_capabilities_for_regular_users: bool | None = field(
        default=None, metadata=field_options(alias="allowContainerCapabilitiesForRegularUsers")
    )
    allow_device_mapping_for_regular_users: bool | None = field(default=None, metadata=field_options(alias="allowDeviceMappingForRegularUsers"))
    allow_host_namespace_for_regular_users: bool | None = field(default=None, metadata=field_options(alias="allowHostNamespaceForRegularUsers"))
    allow_privileged_mode_for_regular_users: bool | None = field(default=None, metadata=field_options(alias="allowPrivilegedModeForRegularUsers"))
    allow_stack_management_for_regular_users: bool | None = field(default=None, metadata=field_options(alias="allowStackManagementForRegularUsers"))
    allow_sysctl_setting_for_regular_users: bool | None = field(default=None, metadata=field_options(alias="allowSysctlSettingForRegularUsers"))
    allow_volume_browser_for_regular_users: bool | None = field(default=None, metadata=field_options(alias="allowVolumeBrowserForRegularUsers"))
    enable_host_management_features: bool | None = field(default=None, metadata=field_options(alias="enableHostManagementFeatures"))


@dataclass
class Agent(DataClassORJSONMixin):
    """Represents agent information."""

    version: str | None = field(default=None, metadata=field_options(alias="version"))


@dataclass
class Edge(DataClassORJSONMixin):
    """Represents edge configuration."""

    command_interval: int | None = field(default=None, metadata=field_options(alias="CommandInterval"))
    ping_interval: int | None = field(default=None, metadata=field_options(alias="PingInterval"))
    snapshot_interval: int | None = field(default=None, metadata=field_options(alias="SnapshotInterval"))
    async_mode: bool | None = field(default=None, metadata=field_options(alias="asyncMode"))


@dataclass
class Endpoint(DataClassORJSONMixin):  # pylint: disable=too-many-instance-attributes
    """Represents a Portainer endpoint."""

    amt_device_guid: str | None = field(default=None, metadata=field_options(alias="AMTDeviceGUID"))
    authorized_teams: list[int] | None = field(default=None, metadata=field_options(alias="AuthorizedTeams"))
    authorized_users: list[int] | None = field(default=None, metadata=field_options(alias="AuthorizedUsers"))
    azure_credentials: dict[str, str] | None = field(default=None, metadata=field_options(alias="AzureCredentials"))
    compose_syntax_max_version: str | None = field(default=None, metadata=field_options(alias="ComposeSyntaxMaxVersion"))
    container_engine: str | None = field(default=None, metadata=field_options(alias="ContainerEngine"))
    edge_checkin_interval: int | None = field(default=None, metadata=field_options(alias="EdgeCheckinInterval"))
    edge_id: str | None = field(default=None, metadata=field_options(alias="EdgeID"))
    edge_key: str | None = field(default=None, metadata=field_options(alias="EdgeKey"))
    enable_gpu_management: bool | None = field(default=None, metadata=field_options(alias="EnableGPUManagement"))
    gpus: list[dict[str, str]] | None = field(default=None, metadata=field_options(alias="Gpus"))
    group_id: int | None = field(default=None, metadata=field_options(alias="GroupId"))
    heartbeat: bool | None = field(default=None, metadata=field_options(alias="Heartbeat"))
    id: int | None = field(default=None, metadata=field_options(alias="Id"))
    is_edge_device: bool | None = field(default=None, metadata=field_options(alias="IsEdgeDevice"))
    kubernetes: dict[str, Any] | None = field(default=None, metadata=field_options(alias="Kubernetes"))
    name: str | None = field(default=None, metadata=field_options(alias="Name"))
    public_url: str | None = field(default=None, metadata=field_options(alias="PublicURL"))
    snapshots: list[dict[str, Any]] | None = field(default=None, metadata=field_options(alias="Snapshots"))
    status: int | None = field(default=None, metadata=field_options(alias="Status"))
    tls: bool | None = field(default=None, metadata=field_options(alias="TLS"))
    tls_ca_cert: str | None = field(default=None, metadata=field_options(alias="TLSCACert"))
    tls_cert: str | None = field(default=None, metadata=field_options(alias="TLSCert"))
    tls_key: str | None = field(default=None, metadata=field_options(alias="TLSKey"))
    tag_ids: list[int] | None = field(default=None, metadata=field_options(alias="TagIds"))
    tags: list[str] | None = field(default=None, metadata=field_options(alias="Tags"))
    team_access_policies: dict[str, dict[str, int]] | None = field(default=None, metadata=field_options(alias="TeamAccessPolicies"))
    type: int | None = field(default=None, metadata=field_options(alias="Type"))
    url: str | None = field(default=None, metadata=field_options(alias="URL"))
    user_access_policies: dict[str, dict[str, int]] | None = field(default=None, metadata=field_options(alias="UserAccessPolicies"))
    user_trusted: bool | None = field(default=None, metadata=field_options(alias="UserTrusted"))
    tls_config: TLSConfig | None = field(default=None, metadata=field_options(alias="TLSConfig"))
    agent: Agent | None = field(default=None, metadata=field_options(alias="agent"))
    edge: Edge | None = field(default=None, metadata=field_options(alias="edge"))
    last_check_in_date: int | None = field(default=None, metadata=field_options(alias="lastCheckInDate"))
    query_date: int | None = field(default=None, metadata=field_options(alias="queryDate"))
    security_settings: SecuritySettings | None = field(default=None, metadata=field_options(alias="securitySettings"))
