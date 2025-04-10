"""Portainer mail model."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import gittypes, v1


class APIKey(DataClassDictMixin):
    """Represents an API key with metadata such as creation date, digest, ID, last used date, prefix, and associated user ID."""

    date_created: int | None = Field(None, alias="dateCreated")
    digest: str | None = Field(None)
    id: int | None = Field(None)
    last_used: int | None = Field(None, alias="lastUsed")
    prefix: str | None = Field(None)
    user_id: int | None = Field(None, alias="userId")


class AccessPolicy(DataClassDictMixin):
    """Represents an access policy with a role ID."""

    role_id: int | None = Field(None, alias="RoleId")


class Authorizations(DataClassDictMixin):
    """Represents a dictionary of authorizations where keys are strings and values are booleans."""

    __root__: dict[str, bool] | None = None


class AutoUpdateSettings(DataClassDictMixin):
    """Represents settings for automatic updates, including force pull image, force update, interval, job ID, and webhook."""

    force_pull_image: bool | None = Field(None, alias="forcePullImage")
    force_update: bool | None = Field(None, alias="forceUpdate")
    interval: str | None = Field(None)
    job_id: str | None = Field(None, alias="jobID")
    webhook: str | None = Field(None)


class AzureCredentials(DataClassDictMixin):
    """Represents Azure credentials with application ID, authentication key, and tenant ID."""

    application_id: str | None = Field(None, alias="ApplicationID")
    authentication_key: str | None = Field(None, alias="AuthenticationKey")
    tenant_id: str | None = Field(None, alias="TenantID")


class CustomTemplateVariableDefinition(DataClassDictMixin):
    """Represents a custom template variable definition with default value, description, label, and name."""

    default_value: str | None = Field(None, alias="defaultValue")
    description: str | None = Field(None)
    label: str | None = Field(None)
    name: str | None = Field(None)


class DiagnosticsData(DataClassDictMixin):
    """Represents diagnostic data including DNS, log, proxy, and telnet information."""

    dns: dict[str, str] | None = Field(None, alias="DNS")
    log: str | None = Field(None, alias="Log")
    proxy: dict[str, str] | None = Field(None, alias="Proxy")
    telnet: dict[str, str] | None = Field(None, alias="Telnet")


class DockerSnapshotRaw(DataClassDictMixin):
    """Represents raw Docker snapshot data."""


class EcrData(DataClassDictMixin):
    """Represents ECR (Elastic Container Registry) data with region information."""

    region: str | None = Field(None, alias="Region")


class Edge(DataClassDictMixin):
    """Represents edge settings including async mode, command interval, ping interval, and snapshot interval."""

    async_mode: bool | None = Field(None, alias="AsyncMode")
    command_interval: int | None = Field(None, alias="CommandInterval")
    ping_interval: int | None = Field(None, alias="PingInterval")
    snapshot_interval: int | None = Field(None, alias="SnapshotInterval")


class EdgeGroup(DataClassDictMixin):
    """Represents an edge group with dynamic status, endpoints, ID, name, partial match, and tag IDs."""

    dynamic: bool | None = Field(None, alias="Dynamic")
    endpoints: list[int] | None = Field(None, alias="Endpoints")
    id: int | None = Field(None, alias="Id")
    name: str | None = Field(None, alias="Name")
    partial_match: bool | None = Field(None, alias="PartialMatch")
    tag_ids: list[int] | None = Field(None, alias="TagIds")


class EdgeJobEndpointMeta(DataClassDictMixin):
    """Represents metadata for an edge job endpoint, including log collection and log status."""

    collect_logs: bool | None = Field(None, alias="collectLogs")
    logs_status: int | None = Field(None, alias="logsStatus")


class EdgeStackDeploymentStatus(DataClassDictMixin):
    """Represents the deployment status of an edge stack, including error, rollback version, and deployment version."""

    error: str | None = Field(None, alias="Error")
    rollback_to: int | None = Field(None, alias="RollbackTo")
    version: int | None = Field(None, alias="Version")
    time: int | None = None
    type: int | None = None


class EdgeStackStatusDetails(DataClassDictMixin):
    """Represents detailed status of an edge stack, including acknowledgment, error, image pull status, and remote update success."""

    acknowledged: bool | None = None
    error: bool | None = None
    images_pulled: bool | None = Field(None, alias="imagesPulled")
    ok: bool | None = None
    pending: bool | None = None
    remote_update_success: bool | None = Field(None, alias="remoteUpdateSuccess")
    remove: bool | None = None


class Agent(DataClassDictMixin):
    """Represents an agent with version information."""

    version: str | None = Field(None)


class EndpointAuthorizations(DataClassDictMixin):
    """Represents endpoint authorizations as a dictionary of authorizations."""

    __root__: dict[str, Authorizations] | None = None


class EndpointPostInitMigrations(DataClassDictMixin):
    """Represents post-initialization migrations for an endpoint, including GPU and ingress migrations."""

    migrate_gp_us: bool | None = Field(None, alias="MigrateGPUs")
    migrate_ingresses: bool | None = Field(None, alias="MigrateIngresses")


class EndpointSecuritySettings(DataClassDictMixin):
    """Represents security settings for an endpoint, including permissions for regular users and host management features."""

    allow_bind_mounts_for_regular_users: bool | None = Field(None, alias="allowBindMountsForRegularUsers")
    allow_container_capabilities_for_regular_users: bool | None = Field(None, alias="allowContainerCapabilitiesForRegularUsers")
    allow_device_mapping_for_regular_users: bool | None = Field(None, alias="allowDeviceMappingForRegularUsers")
    allow_host_namespace_for_regular_users: bool | None = Field(None, alias="allowHostNamespaceForRegularUsers")
    allow_privileged_mode_for_regular_users: bool | None = Field(None, alias="allowPrivilegedModeForRegularUsers")
    allow_stack_management_for_regular_users: bool | None = Field(None, alias="allowStackManagementForRegularUsers")
    allow_sysctl_setting_for_regular_users: bool | None = Field(None, alias="allowSysctlSettingForRegularUsers")
    allow_volume_browser_for_regular_users: bool | None = Field(None, alias="allowVolumeBrowserForRegularUsers")
    enable_host_management_features: bool | None = Field(None, alias="enableHostManagementFeatures")


class EnvironmentEdgeSettings(DataClassDictMixin):
    """Represents edge settings for an environment, including command interval, ping interval, snapshot interval, and async mode."""

    command_interval: int | None = Field(None, alias="CommandInterval")
    ping_interval: int | None = Field(None, alias="PingInterval")
    snapshot_interval: int | None = Field(None, alias="SnapshotInterval")
    async_mode: bool | None = Field(None, alias="asyncMode")


class GitlabRegistryData(DataClassDictMixin):
    """Represents GitLab registry data, including instance URL, project ID, and project path."""

    instance_url: str | None = Field(None, alias="InstanceURL")
    project_id: int | None = Field(None, alias="ProjectId")
    project_path: str | None = Field(None, alias="ProjectPath")


class GlobalDeploymentOptions(DataClassDictMixin):
    """Represents global deployment options, including stack functionality visibility."""

    hide_stacks_functionality: bool | None = Field(None, alias="hideStacksFunctionality")


class HelmUserRepository(DataClassDictMixin):
    """Represents a Helm user repository with ID, URL, and associated user ID."""

    id: int | None = Field(None, alias="Id")
    url: str | None = Field(None, alias="URL")
    user_id: int | None = Field(None, alias="UserId")


class InternalAuthSettings(DataClassDictMixin):
    """Represents internal authentication settings, including required password length."""

    required_password_length: int | None = Field(None, alias="requiredPasswordLength")


class K8sNodeLimits(DataClassDictMixin):
    """Represents Kubernetes node limits, including CPU and memory."""

    cpu: int | None = Field(None, alias="CPU")
    memory: int | None = Field(None, alias="Memory")


class K8sNodesLimits(DataClassDictMixin):
    """Represents Kubernetes nodes limits as a dictionary of node limits."""

    __root__: dict[str, K8sNodeLimits] | None = None


class KubernetesFlags(DataClassDictMixin):
    """Represents Kubernetes flags, including detection of ingress class, metrics, and storage."""

    is_server_ingress_class_detected: bool | None = Field(None, alias="IsServerIngressClassDetected")
    is_server_metrics_detected: bool | None = Field(None, alias="IsServerMetricsDetected")
    is_server_storage_detected: bool | None = Field(None, alias="IsServerStorageDetected")


class KubernetesIngressClassConfig(DataClassDictMixin):
    """Represents Kubernetes ingress class configuration, including blocked status, namespaces, name, and type."""

    blocked: bool | None = Field(None, alias="Blocked")
    blocked_namespaces: list[str] | None = Field(None, alias="BlockedNamespaces")
    name: str | None = Field(None, alias="Name")
    type: str | None = Field(None, alias="Type")


class KubernetesSnapshot(DataClassDictMixin):
    """Represents a Kubernetes snapshot, including diagnostics data, version, node count, and resource usage."""

    diagnostics_data: DiagnosticsData | None = Field(None, alias="DiagnosticsData")
    kubernetes_version: str | None = Field(None, alias="KubernetesVersion")
    node_count: int | None = Field(None, alias="NodeCount")
    time: int | None = Field(None, alias="Time")
    total_cpu: int | None = Field(None, alias="TotalCPU")
    total_memory: int | None = Field(None, alias="TotalMemory")


class KubernetesStorageClassConfig(DataClassDictMixin):
    """Represents Kubernetes storage class configuration, including access modes, volume expansion, name, and provisioner."""

    access_modes: list[str] | None = Field(None, alias="AccessModes")
    allow_volume_expansion: bool | None = Field(None, alias="AllowVolumeExpansion")
    name: str | None = Field(None, alias="Name")
    provisioner: str | None = Field(None, alias="Provisioner")


class LDAPGroupSearchSettings(DataClassDictMixin):
    """Represents LDAP group search settings, including group attribute, base DN, and filter."""

    group_attribute: str | None = Field(None, alias="GroupAttribute")
    group_base_dn: str | None = Field(None, alias="GroupBaseDN")
    group_filter: str | None = Field(None, alias="GroupFilter")


class LDAPSearchSettings(DataClassDictMixin):
    """Represents LDAP search settings, including base DN, filter, and user name attribute."""

    base_dn: str | None = Field(None, alias="BaseDN")
    filter: str | None = Field(None, alias="Filter")
    user_name_attribute: str | None = Field(None, alias="UserNameAttribute")


class OAuthSettings(DataClassDictMixin):
    """Represents OAuth settings, including URIs, client credentials, scopes, and user identifier."""

    access_token_uri: str | None = Field(None, alias="AccessTokenURI")
    auth_style: int | None = Field(None, alias="AuthStyle")
    authorization_uri: str | None = Field(None, alias="AuthorizationURI")
    client_id: str | None = Field(None, alias="ClientID")
    client_secret: str | None = Field(None, alias="ClientSecret")
    default_team_id: int | None = Field(None, alias="DefaultTeamID")
    kube_secret_key: list[int] | None = Field(None, alias="KubeSecretKey")
    logout_uri: str | None = Field(None, alias="LogoutURI")
    o_auth_auto_create_users: bool | None = Field(None, alias="OAuthAutoCreateUsers")
    redirect_uri: str | None = Field(None, alias="RedirectURI")
    resource_uri: str | None = Field(None, alias="ResourceURI")
    sso: bool | None = Field(None, alias="SSO")
    scopes: str | None = Field(None, alias="Scopes")
    user_identifier: str | None = Field(None, alias="UserIdentifier")


class OpenAMTConfiguration(DataClassDictMixin):
    """Represents OpenAMT configuration, including certificate details, domain name, and MPS server settings."""

    cert_file_content: str | None = Field(None, alias="certFileContent")
    cert_file_name: str | None = Field(None, alias="certFileName")
    cert_file_password: str | None = Field(None, alias="certFilePassword")
    domain_name: str | None = Field(None, alias="domainName")
    enabled: bool | None = None
    mps_password: str | None = Field(None, alias="mpsPassword")
    mps_server: str | None = Field(None, alias="mpsServer")
    mps_token: str | None = Field(None, alias="mpsToken")
    mps_user: str | None = Field(None, alias="mpsUser")


class OpenAMTDeviceEnabledFeatures(DataClassDictMixin):
    """Represents enabled features for an OpenAMT device, including IDER, KVM, SOL, and redirection."""

    ider: bool | None = Field(None, alias="IDER")
    kvm: bool | None = Field(None, alias="KVM")
    sol: bool | None = Field(None, alias="SOL")
    redirection: bool | None = None
    user_consent: str | None = Field(None, alias="userConsent")


class Pair(DataClassDictMixin):
    """Represents a key-value pair with name and value."""

    name: str | None = Field(None)
    value: str | None = Field(None)


class QuayRegistryData(DataClassDictMixin):
    """Represents Quay registry data, including organization name and usage settings."""

    organisation_name: str | None = Field(None, alias="OrganisationName")
    use_organisation: bool | None = Field(None, alias="UseOrganisation")


class Role(DataClassDictMixin):
    """Represents a role with authorizations, description, ID, name, and priority."""

    authorizations: Authorizations | None = Field(None, alias="Authorizations")
    description: str | None = Field(None, alias="Description")
    id: int | None = Field(None, alias="Id")
    name: str | None = Field(None, alias="Name")
    priority: int | None = Field(None, alias="Priority")


class SSLSettings(DataClassDictMixin):
    """Represents SSL settings, including certificate path, HTTP enablement, key path, and self-signed status."""

    cert_path: str | None = Field(None, alias="certPath")
    http_enabled: bool | None = Field(None, alias="httpEnabled")
    key_path: str | None = Field(None, alias="keyPath")
    self_signed: bool | None = Field(None, alias="selfSigned")


class StackDeploymentInfo(DataClassDictMixin):
    """Represents stack deployment information, including configuration hash, file version, and deployment version."""

    config_hash: str | None = Field(None, alias="ConfigHash")
    file_version: int | None = Field(None, alias="FileVersion")
    version: int | None = Field(None, alias="Version")


class StackOption(DataClassDictMixin):
    """Represents stack options, including prune settings."""

    prune: bool | None = Field(None)


class TLSConfiguration(DataClassDictMixin):
    """Represents TLS configuration, including certificate details and verification settings."""

    tls: bool | None = Field(None, alias="TLS")
    tlsca_cert: str | None = Field(None, alias="TLSCACert")
    tls_cert: str | None = Field(None, alias="TLSCert")
    tls_key: str | None = Field(None, alias="TLSKey")
    tls_skip_verify: bool | None = Field(None, alias="TLSSkipVerify")


class Tag(DataClassDictMixin):
    """Represents a tag with associated endpoint groups, endpoints, name, and ID."""

    endpoint_groups: dict[str, bool] | None = Field(None, alias="EndpointGroups")
    endpoints: dict[str, bool] | None = Field(None, alias="Endpoints")
    name: str | None = Field(None, alias="Name")
    id: int | None = Field(None)


class Team(DataClassDictMixin):
    """Represents a team with ID and name."""

    id: int | None = Field(None, alias="Id")
    name: str | None = Field(None, alias="Name")


class TeamAccessPolicies(DataClassDictMixin):
    """Represents team access policies as a dictionary of access policies."""

    __root__: dict[str, AccessPolicy] | None = None


class TeamMembership(DataClassDictMixin):
    """Represents team membership with ID, role, team ID, and user ID."""

    id: int | None = Field(None, alias="Id")
    role: int | None = Field(None, alias="Role")
    team_id: int | None = Field(None, alias="TeamID")
    user_id: int | None = Field(None, alias="UserID")


class TeamResourceAccess(DataClassDictMixin):
    """Represents team resource access with access level and team ID."""

    access_level: int | None = Field(None, alias="AccessLevel")
    team_id: int | None = Field(None, alias="TeamId")


class TemplateEnvSelect(DataClassDictMixin):
    """Represents a selectable environment variable for a template, including default status, text, and value."""

    default: bool | None = Field(None)
    text: str | None = Field(None)
    value: str | None = Field(None)


class TemplateRepository(DataClassDictMixin):
    """Represents a template repository with stack file and URL."""

    stackfile: str | None = Field(None)
    url: str | None = Field(None)


class TemplateVolume(DataClassDictMixin):
    """Represents a template volume with bind path, container path, and read-only status."""

    bind: str | None = Field(None)
    container: str | None = Field(None)
    readonly: bool | None = Field(None)


class UserAccessPolicies(DataClassDictMixin):
    """Represents user access policies as a dictionary of access policies."""

    __root__: dict[str, AccessPolicy] | None = None


class UserResourceAccess(DataClassDictMixin):
    """Represents user resource access with access level and user ID."""

    access_level: int | None = Field(None, alias="AccessLevel")
    user_id: int | None = Field(None, alias="UserId")


class Color(Enum):
    """Represents color options for user theme settings."""

    dark = "dark"  # pylint: disable=C0103
    light = "light"  # pylint: disable=C0103
    highcontrast = "highcontrast"  # pylint: disable=C0103
    auto = "auto"  # pylint: disable=C0103


class UserThemeSettings(DataClassDictMixin):
    """Represents user theme settings, including color."""

    color: Color | None = Field(None)


class Webhook(DataClassDictMixin):
    """Represents a webhook with endpoint ID, registry ID, resource ID, token, and type."""

    endpoint_id: int | None = Field(None, alias="EndpointId")
    id: int | None = Field(None, alias="Id")
    registry_id: int | None = Field(None, alias="RegistryId")
    resource_id: str | None = Field(None, alias="ResourceId")
    token: str | None = Field(None, alias="Token")
    type: int | None = Field(None, alias="Type")


class DockerSnapshot(DataClassDictMixin):
    """Represents a Docker snapshot, including container count, diagnostics data, Docker version, and resource usage."""

    container_count: int | None = Field(None, alias="ContainerCount")
    diagnostics_data: DiagnosticsData | None = Field(None, alias="DiagnosticsData")
    docker_snapshot_raw: DockerSnapshotRaw | None = Field(None, alias="DockerSnapshotRaw")
    docker_version: str | None = Field(None, alias="DockerVersion")
    gpu_use_all: bool | None = Field(None, alias="GpuUseAll")
    gpu_use_list: list[str] | None = Field(None, alias="GpuUseList")
    healthy_container_count: int | None = Field(None, alias="HealthyContainerCount")
    image_count: int | None = Field(None, alias="ImageCount")
    is_podman: bool | None = Field(None, alias="IsPodman")
    node_count: int | None = Field(None, alias="NodeCount")
    running_container_count: int | None = Field(None, alias="RunningContainerCount")
    service_count: int | None = Field(None, alias="ServiceCount")
    stack_count: int | None = Field(None, alias="StackCount")
    stopped_container_count: int | None = Field(None, alias="StoppedContainerCount")
    swarm: bool | None = Field(None, alias="Swarm")
    time: int | None = Field(None, alias="Time")
    total_cpu: int | None = Field(None, alias="TotalCPU")
    total_memory: int | None = Field(None, alias="TotalMemory")
    unhealthy_container_count: int | None = Field(None, alias="UnhealthyContainerCount")
    volume_count: int | None = Field(None, alias="VolumeCount")


class EdgeJob(DataClassDictMixin):
    """Represents an edge job, including creation date, cron expression, edge groups, endpoints, ID, name, and version."""

    created: int | None = Field(None, alias="Created")
    cron_expression: str | None = Field(None, alias="CronExpression")
    edge_groups: list[int] | None = Field(None, alias="EdgeGroups")
    endpoints: dict[str, EdgeJobEndpointMeta] | None = Field(None, alias="Endpoints")
    id: int | None = Field(None, alias="Id")
    name: str | None = Field(None, alias="Name")
    recurring: bool | None = Field(None, alias="Recurring")
    script_path: str | None = Field(None, alias="ScriptPath")
    version: int | None = Field(None, alias="Version")
    group_logs_collection: dict[str, EdgeJobEndpointMeta] | None = Field(None, alias="groupLogsCollection")


class EdgeStackStatus(DataClassDictMixin):
    """Represents the status of an edge stack, including details, error, readiness, type, deployment info, and endpoint ID."""

    details: EdgeStackStatusDetails | None = Field(None, alias="Details")
    error: str | None = Field(None, alias="Error")
    ready_re_pull_image: bool | None = Field(None, alias="ReadyRePullImage")
    type: int | None = Field(None, alias="Type")
    deployment_info: StackDeploymentInfo | None = Field(None, alias="deploymentInfo")
    endpoint_id: int | None = Field(None, alias="endpointID")
    status: list[EdgeStackDeploymentStatus] | None = None


class EndpointGroup(DataClassDictMixin):
    """Represents an endpoint group, including authorized teams, users, description, ID, labels, name, tags, and access policies."""

    authorized_teams: list[int] | None = Field(None, alias="AuthorizedTeams")
    authorized_users: list[int] | None = Field(None, alias="AuthorizedUsers")
    description: str | None = Field(None, alias="Description")
    id: int | None = Field(None, alias="Id")
    labels: list[Pair] | None = Field(None, alias="Labels")
    name: str | None = Field(None, alias="Name")
    tag_ids: list[int] | None = Field(None, alias="TagIds")
    tags: list[str] | None = Field(None, alias="Tags")
    team_access_policies: TeamAccessPolicies | None = Field(None, alias="TeamAccessPolicies")
    user_access_policies: UserAccessPolicies | None = Field(None, alias="UserAccessPolicies")


class KubernetesConfiguration(DataClassDictMixin):
    """Represents Kubernetes configuration, including ingress classes, storage classes, and resource over-commit settings."""

    allow_none_ingress_class: bool | None = Field(None, alias="AllowNoneIngressClass")
    enable_resource_over_commit: bool | None = Field(None, alias="EnableResourceOverCommit")
    ingress_availability_per_namespace: bool | None = Field(None, alias="IngressAvailabilityPerNamespace")
    ingress_classes: list[KubernetesIngressClassConfig] | None = Field(None, alias="IngressClasses")
    resource_over_commit_percentage: int | None = Field(None, alias="ResourceOverCommitPercentage")
    restrict_default_namespace: bool | None = Field(None, alias="RestrictDefaultNamespace")
    storage_classes: list[KubernetesStorageClassConfig] | None = Field(None, alias="StorageClasses")
    use_load_balancer: bool | None = Field(None, alias="UseLoadBalancer")
    use_server_metrics: bool | None = Field(None, alias="UseServerMetrics")


class KubernetesData(DataClassDictMixin):
    """Represents Kubernetes data, including configuration, flags, and snapshots."""

    configuration: KubernetesConfiguration | None = Field(None, alias="Configuration")
    flags: KubernetesFlags | None = Field(None, alias="Flags")
    snapshots: list[KubernetesSnapshot] | None = Field(None, alias="Snapshots")


class LDAPSettings(DataClassDictMixin):
    """Represents LDAP settings, including anonymous mode, auto-create users, group search settings, and TLS configuration."""

    anonymous_mode: bool | None = Field(None, alias="AnonymousMode")
    auto_create_users: bool | None = Field(None, alias="AutoCreateUsers")
    group_search_settings: list[LDAPGroupSearchSettings] | None = Field(None, alias="GroupSearchSettings")
    password: str | None = Field(None, alias="Password")
    reader_dn: str | None = Field(None, alias="ReaderDN")
    search_settings: list[LDAPSearchSettings] | None = Field(None, alias="SearchSettings")
    start_tls: bool | None = Field(None, alias="StartTLS")
    tls_config: TLSConfiguration | None = Field(None, alias="TLSConfig")
    url: str | None = Field(None, alias="URL")


class RegistryAccessPolicies(DataClassDictMixin):
    """Represents registry access policies, including namespaces, team access policies, and user access policies."""

    namespaces: list[str] | None = Field(None, alias="Namespaces")
    team_access_policies: TeamAccessPolicies | None = Field(None, alias="TeamAccessPolicies")
    user_access_policies: UserAccessPolicies | None = Field(None, alias="UserAccessPolicies")


class RegistryAccesses(DataClassDictMixin):
    """Represents registry accesses as a dictionary of access policies."""

    __root__: dict[str, RegistryAccessPolicies] | None = None


class RegistryManagementConfiguration(DataClassDictMixin):
    """Represents registry management configuration, including authentication, ECR data, and TLS configuration."""

    access_token: str | None = Field(None, alias="AccessToken")
    access_token_expiry: int | None = Field(None, alias="AccessTokenExpiry")
    authentication: bool | None = Field(None, alias="Authentication")
    ecr: EcrData | None = Field(None, alias="Ecr")
    password: str | None = Field(None, alias="Password")
    tls_config: TLSConfiguration | None = Field(None, alias="TLSConfig")
    type: int | None = Field(None, alias="Type")
    username: str | None = Field(None, alias="Username")


class ResourceControl(DataClassDictMixin):
    """Represents resource control settings, including access level, ownership, and access policies."""

    access_level: int | None = Field(None, alias="AccessLevel")
    administrators_only: bool | None = Field(None, alias="AdministratorsOnly")
    id: int | None = Field(None, alias="Id")
    owner_id: int | None = Field(None, alias="OwnerId")
    public: bool | None = Field(None, alias="Public")
    resource_id: str | None = Field(None, alias="ResourceId")
    sub_resource_ids: list[str] | None = Field(None, alias="SubResourceIds")
    system: bool | None = Field(None, alias="System")
    team_accesses: list[TeamResourceAccess] | None = Field(None, alias="TeamAccesses")
    type: int | None = Field(None, alias="Type")
    user_accesses: list[UserResourceAccess] | None = Field(None, alias="UserAccesses")


class Settings(DataClassDictMixin):
    """Represents application settings, including agent secret, authentication method, edge settings, and feature flags."""

    agent_secret: str | None = Field(None, alias="AgentSecret")
    allow_bind_mounts_for_regular_users: bool | None = Field(None, alias="AllowBindMountsForRegularUsers")
    allow_container_capabilities_for_regular_users: bool | None = Field(None, alias="AllowContainerCapabilitiesForRegularUsers")
    allow_device_mapping_for_regular_users: bool | None = Field(None, alias="AllowDeviceMappingForRegularUsers")
    allow_host_namespace_for_regular_users: bool | None = Field(None, alias="AllowHostNamespaceForRegularUsers")
    allow_privileged_mode_for_regular_users: bool | None = Field(None, alias="AllowPrivilegedModeForRegularUsers")
    allow_stack_management_for_regular_users: bool | None = Field(None, alias="AllowStackManagementForRegularUsers")
    allow_volume_browser_for_regular_users: bool | None = Field(None, alias="AllowVolumeBrowserForRegularUsers")
    authentication_method: int | None = Field(None, alias="AuthenticationMethod")
    black_listed_labels: list[Pair] | None = Field(None, alias="BlackListedLabels")
    display_donation_header: bool | None = Field(None, alias="DisplayDonationHeader")
    display_external_contributors: bool | None = Field(None, alias="DisplayExternalContributors")
    edge: Edge | None = Field(None, alias="Edge")
    edge_agent_checkin_interval: int | None = Field(None, alias="EdgeAgentCheckinInterval")
    edge_portainer_url: str | None = Field(None, alias="EdgePortainerUrl")
    enable_edge_compute_features: bool | None = Field(None, alias="EnableEdgeComputeFeatures")
    enable_host_management_features: bool | None = Field(None, alias="EnableHostManagementFeatures")
    enable_telemetry: bool | None = Field(None, alias="EnableTelemetry")
    enforce_edge_id: bool | None = Field(None, alias="EnforceEdgeID")
    feature_flag_settings: dict[str, bool] | None = Field(None, alias="FeatureFlagSettings")
    global_deployment_options: GlobalDeploymentOptions | None = Field(None, alias="GlobalDeploymentOptions")
    helm_repository_url: str | None = Field(None, alias="HelmRepositoryURL")
    internal_auth_settings: InternalAuthSettings | None = Field(None, alias="InternalAuthSettings")
    is_docker_desktop_extension: bool | None = Field(None, alias="IsDockerDesktopExtension")
    kubeconfig_expiry: str | None = Field(None, alias="KubeconfigExpiry")
    kubectl_shell_image: str | None = Field(None, alias="KubectlShellImage")
    ldap_settings: LDAPSettings | None = Field(None, alias="LDAPSettings")
    logo_url: str | None = Field(None, alias="LogoURL")
    o_auth_settings: OAuthSettings | None = Field(None, alias="OAuthSettings")
    snapshot_interval: str | None = Field(None, alias="SnapshotInterval")
    templates_url: str | None = Field(None, alias="TemplatesURL")
    trust_on_first_connect: bool | None = Field(None, alias="TrustOnFirstConnect")
    user_session_timeout: str | None = Field(None, alias="UserSessionTimeout")
    open_amt_configuration: OpenAMTConfiguration | None = Field(None, alias="openAMTConfiguration")


class Stack(DataClassDictMixin):
    """Represents a stack, including additional files, auto-update settings, endpoint ID, entry point, environment variables, and resource control."""

    additional_files: list[str] | None = Field(None, alias="AdditionalFiles")
    auto_update: AutoUpdateSettings | None = Field(None, alias="AutoUpdate")
    endpoint_id: int | None = Field(None, alias="EndpointId")
    entry_point: str | None = Field(None, alias="EntryPoint")
    env: list[Pair] | None = Field(None, alias="Env")
    id: int | None = Field(None, alias="Id")
    name: str | None = Field(None, alias="Name")
    option: StackOption | None = Field(None, alias="Option")
    resource_control: ResourceControl | None = Field(None, alias="ResourceControl")
    status: int | None = Field(None, alias="Status")
    swarm_id: str | None = Field(None, alias="SwarmId")
    type: int | None = Field(None, alias="Type")
    created_by: str | None = Field(None, alias="createdBy")
    creation_date: int | None = Field(None, alias="creationDate")
    from_app_template: bool | None = Field(None, alias="fromAppTemplate")
    git_config: gittypes.RepoConfig | None = Field(None, alias="gitConfig")
    namespace: str | None = Field(None)
    project_path: str | None = Field(None, alias="projectPath")
    update_date: int | None = Field(None, alias="updateDate")
    updated_by: str | None = Field(None, alias="updatedBy")


class TemplateEnv(DataClassDictMixin):
    """Represents a template environment variable, including default value, description, label, and name."""

    default: str | None = Field(None)
    description: str | None = Field(None)
    label: str | None = Field(None)
    name: str | None = Field(None)
    preset: bool | None = Field(None)
    select: list[TemplateEnvSelect] | None = Field(None)


class User(DataClassDictMixin):
    """Represents a user, including ID, role, theme settings, token issue date, cache usage, and authorizations."""

    id: int | None = Field(None, alias="Id")
    role: int | None = Field(None, alias="Role")
    theme_settings: UserThemeSettings | None = Field(None, alias="ThemeSettings")
    token_issue_at: int | None = Field(None, alias="TokenIssueAt")
    use_cache: bool | None = Field(None, alias="UseCache")
    user_theme: str | None = Field(None, alias="UserTheme")
    username: str | None = Field(None, alias="Username")
    endpoint_authorizations: EndpointAuthorizations | None = Field(None, alias="endpointAuthorizations")
    portainer_authorizations: Authorizations | None = Field(None, alias="portainerAuthorizations")


class CustomTemplate(DataClassDictMixin):
    """Represents a custom template, including creator ID, description, entry point, Git configuration, ID, logo, note, platform, and variables."""

    created_by_user_id: int | None = Field(None, alias="CreatedByUserId")
    description: str | None = Field(None, alias="Description")
    entry_point: str | None = Field(None, alias="EntryPoint")
    git_config: gittypes.RepoConfig | None = Field(None, alias="GitConfig")
    id: int | None = Field(None, alias="Id")
    logo: str | None = Field(None, alias="Logo")
    note: str | None = Field(None, alias="Note")
    platform: int | None = Field(None, alias="Platform")
    project_path: str | None = Field(None, alias="ProjectPath")
    resource_control: ResourceControl | None = Field(None, alias="ResourceControl")
    title: str | None = Field(None, alias="Title")
    type: int | None = Field(None, alias="Type")
    edge_template: bool | None = Field(None, alias="edgeTemplate")
    is_compose_format: bool | None = Field(None, alias="isComposeFormat")
    variables: list[CustomTemplateVariableDefinition] | None = None


class EdgeStack(DataClassDictMixin):
    """Represents an edge stack, including creation date, deployment type, edge groups, entry point, ID, manifest path, name, and version."""

    creation_date: int | None = Field(None, alias="CreationDate")
    deployment_type: int | None = Field(None, alias="DeploymentType")
    edge_groups: list[int] | None = Field(None, alias="EdgeGroups")
    entry_point: str | None = Field(None, alias="EntryPoint")
    id: int | None = Field(None, alias="Id")
    manifest_path: str | None = Field(None, alias="ManifestPath")
    name: str | None = Field(None, alias="Name")
    num_deployments: int | None = Field(None, alias="NumDeployments")
    project_path: str | None = Field(None, alias="ProjectPath")
    status: dict[str, EdgeStackStatus] | None = Field(None, alias="Status")
    version: int | None = Field(None, alias="Version")
    use_manifest_namespaces: bool | None = Field(None, alias="useManifestNamespaces")


class Endpoint(DataClassDictMixin):
    """Represents an endpoint, including device GUID, authorized teams and users, credentials, engine, edge settings, and snapshots."""

    amt_device_guid: str | None = Field(None, alias="AMTDeviceGUID")
    authorized_teams: list[int] | None = Field(None, alias="AuthorizedTeams")
    authorized_users: list[int] | None = Field(None, alias="AuthorizedUsers")
    azure_credentials: AzureCredentials | None = Field(None, alias="AzureCredentials")
    compose_syntax_max_version: str | None = Field(None, alias="ComposeSyntaxMaxVersion")
    container_engine: str | None = Field(None, alias="ContainerEngine")
    edge_checkin_interval: int | None = Field(None, alias="EdgeCheckinInterval")
    edge_id: str | None = Field(None, alias="EdgeID")
    edge_key: str | None = Field(None, alias="EdgeKey")
    enable_gpu_management: bool | None = Field(None, alias="EnableGPUManagement")
    gpus: list[Pair] | None = Field(None, alias="Gpus")
    group_id: int | None = Field(None, alias="GroupId")
    heartbeat: bool | None = Field(None, alias="Heartbeat")
    id: int | None = Field(None, alias="Id")
    is_edge_device: bool | None = Field(None, alias="IsEdgeDevice")
    kubernetes: KubernetesData | None = Field(None, alias="Kubernetes")
    name: str | None = Field(None, alias="Name")
    post_init_migrations: EndpointPostInitMigrations | None = Field(None, alias="PostInitMigrations")
    public_url: str | None = Field(None, alias="PublicURL")
    snapshots: list[DockerSnapshot] | None = Field(None, alias="Snapshots")
    status: int | None = Field(None, alias="Status")
    tls: bool | None = Field(None, alias="TLS")
    tlsca_cert: str | None = Field(None, alias="TLSCACert")
    tls_cert: str | None = Field(None, alias="TLSCert")
    tls_config: TLSConfiguration | None = Field(None, alias="TLSConfig")
    tls_key: str | None = Field(None, alias="TLSKey")
    tag_ids: list[int] | None = Field(None, alias="TagIds")
    tags: list[str] | None = Field(None, alias="Tags")
    team_access_policies: TeamAccessPolicies | None = Field(None, alias="TeamAccessPolicies")
    type: int | None = Field(None, alias="Type")
    url: str | None = Field(None, alias="URL")
    user_access_policies: UserAccessPolicies | None = Field(None, alias="UserAccessPolicies")
    user_trusted: bool | None = Field(None, alias="UserTrusted")
    agent: Agent | None = None
    edge: EnvironmentEdgeSettings | None = None
    last_check_in_date: int | None = Field(None, alias="lastCheckInDate")
    query_date: int | None = Field(None, alias="queryDate")
    security_settings: EndpointSecuritySettings | None = Field(None, alias="securitySettings")


class Registry(DataClassDictMixin):
    """Represents a registry, including access token, authentication, authorized teams and users, base URL, and management configuration."""

    access_token: str | None = Field(None, alias="AccessToken")
    access_token_expiry: int | None = Field(None, alias="AccessTokenExpiry")
    authentication: bool | None = Field(None, alias="Authentication")
    authorized_teams: list[int] | None = Field(None, alias="AuthorizedTeams")
    authorized_users: list[int] | None = Field(None, alias="AuthorizedUsers")
    base_url: str | None = Field(None, alias="BaseURL")
    ecr: EcrData | None = Field(None, alias="Ecr")
    gitlab: GitlabRegistryData | None = Field(None, alias="Gitlab")
    id: int | None = Field(None, alias="Id")
    management_configuration: RegistryManagementConfiguration | None = Field(None, alias="ManagementConfiguration")
    name: str | None = Field(None, alias="Name")
    password: str | None = Field(None, alias="Password")
    quay: QuayRegistryData | None = Field(None, alias="Quay")
    registry_accesses: RegistryAccesses | None = Field(None, alias="RegistryAccesses")
    team_access_policies: TeamAccessPolicies | None = Field(None, alias="TeamAccessPolicies")
    type: int | None = Field(None, alias="Type")
    url: str | None = Field(None, alias="URL")
    user_access_policies: UserAccessPolicies | None = Field(None, alias="UserAccessPolicies")
    username: str | None = Field(None, alias="Username")


class Template(DataClassDictMixin):
    """Represents a template, including administrator-only status, categories, command, description, environment variables, and repository."""

    administrator_only: bool | None = Field(None)
    categories: list[str] | None = Field(None)
    command: str | None = Field(None)
    description: str | None = Field(None)
    env: list[TemplateEnv] | None = Field(None)
    hostname: str | None = Field(None)
    id: int | None = Field(None)
    image: str | None = Field(None)
    interactive: bool | None = Field(None)
    labels: list[Pair] | None = Field(None)
    logo: str | None = Field(None)
    name: str | None = Field(None)
    network: str | None = Field(None)
    note: str | None = Field(None)
    platform: str | None = Field(None)
    ports: list[str] | None = Field(None)
    privileged: bool | None = Field(None)
    registry: str | None = Field(None)
    repository: TemplateRepository | None = None
    restart_policy: str | None = Field(None)
    stack_file: str | None = Field(None, alias="stackFile")
    title: str | None = Field(None)
    type: int | None = Field(None)
    volumes: list[TemplateVolume] | None = Field(None)


class K8sNamespaceInfo(DataClassDictMixin):
    """Represents Kubernetes namespace information, including annotations, creation date, ID, default status, and resource quota."""

    annotations: dict[str, str] | None = Field(None, alias="Annotations")
    creation_date: str | None = Field(None, alias="CreationDate")
    id: str | None = Field(None, alias="Id")
    is_default: bool | None = Field(None, alias="IsDefault")
    is_system: bool | None = Field(None, alias="IsSystem")
    name: str | None = Field(None, alias="Name")
    namespace_owner: str | None = Field(None, alias="NamespaceOwner")
    resource_quota: v1.ResourceQuota | None = Field(None, alias="ResourceQuota")
    status: v1.NamespaceStatus | None = Field(None, alias="Status")
