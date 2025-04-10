"""Data models for Kubernetes v1 API objects in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import intstr
    from . import resource as resource_1


class ExecAction(DataClassDictMixin):
    """Executes a command inside a container."""

    command: list[str] | None = Field(None)


class AppArmorProfile(DataClassDictMixin):
    """Represents an AppArmor profile configuration."""

    localhost_profile: str | None = Field(None, alias="localhostProfile")
    type: str | None = Field(None)


class Capabilities(DataClassDictMixin):
    """Represents Linux capabilities to add or drop."""

    add: list[str] | None = Field(None)
    drop: list[str] | None = Field(None)


class ClientIPConfig(DataClassDictMixin):
    """Configuration for ClientIP session affinity."""

    timeout_seconds: int | None = Field(None, alias="timeoutSeconds")


class Condition(DataClassDictMixin):
    """Represents a condition of a Kubernetes object."""

    last_transition_time: str | None = Field(None, alias="lastTransitionTime")
    message: str | None = Field(None)
    observed_generation: int | None = Field(None, alias="observedGeneration")
    reason: str | None = Field(None)
    status: str | None = Field(None)
    type: str | None = Field(None)


class ConfigMapEnvSource(DataClassDictMixin):
    """Represents a source for environment variables from a ConfigMap."""

    name: str | None = Field(None)
    optional: bool | None = Field(None)


class ConfigMapKeySelector(DataClassDictMixin):
    """Selects a key from a ConfigMap."""

    key: str | None = Field(None)
    name: str | None = Field(None)
    optional: bool | None = Field(None)


class ContainerPort(DataClassDictMixin):
    """Represents a container port."""

    container_port: int | None = Field(None, alias="containerPort")
    host_ip: str | None = Field(None, alias="hostIP")
    host_port: int | None = Field(None, alias="hostPort")
    name: str | None = Field(None)
    protocol: str | None = Field(None)


class ContainerResizePolicy(DataClassDictMixin):
    """Policy for resizing container resources."""

    resource_name: str | None = Field(None, alias="resourceName")
    restart_policy: str | None = Field(None, alias="restartPolicy")


class Duration(DataClassDictMixin):
    """Represents a duration in seconds."""

    time_duration: int | None = Field(None, alias="time.Duration")


class FieldsV1(DataClassDictMixin):
    """Represents fields in Kubernetes objects."""


class GRPCAction(DataClassDictMixin):
    """Represents a gRPC action."""

    port: int | None = Field(None)
    service: str | None = Field(None)


class HTTPHeader(DataClassDictMixin):
    """Represents an HTTP header."""

    name: str | None = Field(None)
    value: str | None = Field(None)


class LabelSelectorRequirement(DataClassDictMixin):
    """Represents a label selector requirement."""

    key: str | None = Field(None)
    operator: str | None = Field(None)
    values: list[str] | None = Field(None)


class ManagedFieldsEntry(DataClassDictMixin):
    """Represents managed fields in Kubernetes objects."""

    api_version: str | None = Field(None, alias="apiVersion")
    fields_type: str | None = Field(None, alias="fieldsType")
    fields_v1: FieldsV1 | None = Field(None, alias="fieldsV1")
    manager: str | None = Field(None)
    operation: str | None = Field(None)
    subresource: str | None = Field(None)
    time: str | None = Field(None)


class NamespaceCondition(DataClassDictMixin):
    """Represents a condition of a namespace."""

    last_transition_time: str | None = Field(None, alias="lastTransitionTime")
    message: str | None = Field(None)
    reason: str | None = Field(None)
    status: str | None = Field(None)
    type: str | None = Field(None)


class NamespaceStatus(DataClassDictMixin):
    """Represents the status of a namespace."""

    conditions: list[NamespaceCondition] | None = Field(None)
    phase: str | None = Field(None)


class ObjectFieldSelector(DataClassDictMixin):
    """Selects a field from an object."""

    api_version: str | None = Field(None, alias="apiVersion")
    field_path: str | None = Field(None, alias="fieldPath")


class ObjectReference(DataClassDictMixin):
    """Represents a reference to a Kubernetes object."""

    api_version: str | None = Field(None, alias="apiVersion")
    field_path: str | None = Field(None, alias="fieldPath")
    kind: str | None = Field(None)
    name: str | None = Field(None)
    namespace: str | None = Field(None)
    resource_version: str | None = Field(None, alias="resourceVersion")
    uid: str | None = Field(None)


class OwnerReference(DataClassDictMixin):
    """Represents an owner reference for garbage collection."""

    api_version: str | None = Field(None, alias="apiVersion")
    block_owner_deletion: bool | None = Field(None, alias="blockOwnerDeletion")
    controller: bool | None = Field(None)
    kind: str | None = Field(None)
    name: str | None = Field(None)
    uid: str | None = Field(None)


class PortStatus(DataClassDictMixin):
    """Represents the status of a service port."""

    error: str | None = Field(None)
    port: int | None = Field(None)
    protocol: str | None = Field(None)


class ResourceClaim(DataClassDictMixin):
    """Represents a resource claim."""

    name: str | None = Field(None)
    request: str | None = Field(None)


class ResourceFieldSelector(DataClassDictMixin):
    """Selects a resource field."""

    container_name: str | None = Field(None, alias="containerName")
    divisor: resource_1.Quantity | None = None
    resource: str | None = Field(None)


class ResourceList(DataClassDictMixin):
    """Represents a list of resources."""

    __root__: dict[str, resource_1.Quantity] | None = None


class ResourceQuotaStatus(DataClassDictMixin):
    """Represents the status of a resource quota."""

    hard: ResourceList | None = None
    used: ResourceList | None = None


class ResourceRequirements(DataClassDictMixin):
    """Represents resource requirements for a container."""

    claims: list[ResourceClaim] | None = Field(None)
    limits: ResourceList | None = None
    requests: ResourceList | None = None


class RoleRef(DataClassDictMixin):
    """Represents a reference to a role."""

    api_group: str | None = Field(None, alias="apiGroup")
    kind: str | None = Field(None)
    name: str | None = Field(None)


class SELinuxOptions(DataClassDictMixin):
    """Represents SELinux options."""

    level: str | None = Field(None)
    role: str | None = Field(None)
    type: str | None = Field(None)
    user: str | None = Field(None)


class ScopedResourceSelectorRequirement(DataClassDictMixin):
    """Represents a scoped resource selector requirement."""

    operator: str | None = Field(None)
    scope_name: str | None = Field(None, alias="scopeName")
    values: list[str] | None = Field(None)


class SeccompProfile(DataClassDictMixin):
    """Represents a seccomp profile configuration."""

    localhost_profile: str | None = Field(None, alias="localhostProfile")
    type: str | None = Field(None)


class SecretEnvSource(DataClassDictMixin):
    """Represents a source for environment variables from a Secret."""

    name: str | None = Field(None)
    optional: bool | None = Field(None)


class SecretKeySelector(DataClassDictMixin):
    """Selects a key from a Secret."""

    key: str | None = Field(None)
    name: str | None = Field(None)
    optional: bool | None = Field(None)


class SecretReference(DataClassDictMixin):
    """Represents a reference to a Secret."""

    name: str | None = Field(None)
    namespace: str | None = Field(None)


class ServicePort(DataClassDictMixin):
    """Represents a service port."""

    app_protocol: str | None = Field(None, alias="appProtocol")
    name: str | None = Field(None)
    node_port: int | None = Field(None, alias="nodePort")
    port: int | None = Field(None)
    protocol: str | None = Field(None)
    target_port: intstr.IntOrString | None = Field(None, alias="targetPort")


class SessionAffinityConfig(DataClassDictMixin):
    """Represents session affinity configuration."""

    client_ip: ClientIPConfig | None = Field(None, alias="clientIP")


class SleepAction(DataClassDictMixin):
    """Represents a sleep action."""

    seconds: int | None = Field(None)


class Subject(DataClassDictMixin):
    """Represents a subject in RBAC."""

    api_group: str | None = Field(None, alias="apiGroup")
    kind: str | None = Field(None)
    name: str | None = Field(None)
    namespace: str | None = Field(None)


class TCPSocketAction(DataClassDictMixin):
    """Represents a TCP socket action."""

    host: str | None = Field(None)
    port: intstr.IntOrString | None = None


class VolumeDevice(DataClassDictMixin):
    """Represents a block device to be used by a container."""

    device_path: str | None = Field(None, alias="devicePath")
    name: str | None = Field(None)


class VolumeMount(DataClassDictMixin):
    """Represents a volume mount."""

    mount_path: str | None = Field(None, alias="mountPath")
    mount_propagation: str | None = Field(None, alias="mountPropagation")
    name: str | None = Field(None)
    read_only: bool | None = Field(None, alias="readOnly")
    recursive_read_only: str | None = Field(None, alias="recursiveReadOnly")
    sub_path: str | None = Field(None, alias="subPath")
    sub_path_expr: str | None = Field(None, alias="subPathExpr")


class WindowsSecurityContextOptions(DataClassDictMixin):
    """Represents Windows security context options."""

    gmsa_credential_spec: str | None = Field(None, alias="gmsaCredentialSpec")
    gmsa_credential_spec_name: str | None = Field(None, alias="gmsaCredentialSpecName")
    host_process: bool | None = Field(None, alias="hostProcess")
    run_as_user_name: str | None = Field(None, alias="runAsUserName")


class CSIPersistentVolumeSource(DataClassDictMixin):
    """Represents a CSI persistent volume source."""

    controller_expand_secret_ref: SecretReference | None = Field(None, alias="controllerExpandSecretRef")
    controller_publish_secret_ref: SecretReference | None = Field(None, alias="controllerPublishSecretRef")
    driver: str | None = Field(None)
    fs_type: str | None = Field(None, alias="fsType")
    node_expand_secret_ref: SecretReference | None = Field(None, alias="nodeExpandSecretRef")
    node_publish_secret_ref: SecretReference | None = Field(None, alias="nodePublishSecretRef")
    node_stage_secret_ref: SecretReference | None = Field(None, alias="nodeStageSecretRef")
    read_only: bool | None = Field(None, alias="readOnly")
    volume_attributes: dict[str, str] | None = Field(None, alias="volumeAttributes")
    volume_handle: str | None = Field(None, alias="volumeHandle")


class EnvFromSource(DataClassDictMixin):
    """Represents a source for environment variables."""

    config_map_ref: ConfigMapEnvSource | None = Field(None, alias="configMapRef")
    prefix: str | None = Field(None)
    secret_ref: SecretEnvSource | None = Field(None, alias="secretRef")


class EnvVarSource(DataClassDictMixin):
    """Represents a source for an environment variable."""

    config_map_key_ref: ConfigMapKeySelector | None = Field(None, alias="configMapKeyRef")
    field_ref: ObjectFieldSelector | None = Field(None, alias="fieldRef")
    resource_field_ref: ResourceFieldSelector | None = Field(None, alias="resourceFieldRef")
    secret_key_ref: SecretKeySelector | None = Field(None, alias="secretKeyRef")


class HTTPGetAction(DataClassDictMixin):
    """Represents an HTTP GET action."""

    host: str | None = Field(None)
    http_headers: list[HTTPHeader] | None = Field(None, alias="httpHeaders")
    path: str | None = Field(None)
    port: intstr.IntOrString | None = None
    scheme: str | None = Field(None)


class LabelSelector(DataClassDictMixin):
    """Represents a label selector."""

    match_expressions: list[LabelSelectorRequirement] | None = Field(None, alias="matchExpressions")
    match_labels: dict[str, str] | None = Field(None, alias="matchLabels")


class LifecycleHandler(DataClassDictMixin):
    """Represents a lifecycle handler."""

    exec: ExecAction | None = None
    http_get: HTTPGetAction | None = Field(None, alias="httpGet")
    sleep: SleepAction | None = None
    tcp_socket: TCPSocketAction | None = Field(None, alias="tcpSocket")


class LoadBalancerIngress(DataClassDictMixin):
    """Represents ingress points for a load balancer."""

    hostname: str | None = Field(None)
    ip: str | None = Field(None)
    ip_mode: str | None = Field(None, alias="ipMode")
    ports: list[PortStatus] | None = Field(None)


class LoadBalancerStatus(DataClassDictMixin):
    """Represents the status of a load balancer."""

    ingress: list[LoadBalancerIngress] | None = Field(None)


class Probe(DataClassDictMixin):
    """Represents a probe for container health checks."""

    exec: ExecAction | None = None
    failure_threshold: int | None = Field(None, alias="failureThreshold")
    grpc: GRPCAction | None = None
    http_get: HTTPGetAction | None = Field(None, alias="httpGet")
    initial_delay_seconds: int | None = Field(None, alias="initialDelaySeconds")
    period_seconds: int | None = Field(None, alias="periodSeconds")
    success_threshold: int | None = Field(None, alias="successThreshold")
    tcp_socket: TCPSocketAction | None = Field(None, alias="tcpSocket")
    termination_grace_period_seconds: int | None = Field(None, alias="terminationGracePeriodSeconds")
    timeout_seconds: int | None = Field(None, alias="timeoutSeconds")


class ScopeSelector(DataClassDictMixin):
    """Represents a scope selector."""

    match_expressions: list[ScopedResourceSelectorRequirement] | None = Field(None, alias="matchExpressions")


class SecurityContext(DataClassDictMixin):
    """Represents security context settings for a container."""

    allow_privilege_escalation: bool | None = Field(None, alias="allowPrivilegeEscalation")
    app_armor_profile: AppArmorProfile | None = Field(None, alias="appArmorProfile")
    capabilities: Capabilities | None = None
    privileged: bool | None = Field(None)
    proc_mount: str | None = Field(None, alias="procMount")
    read_only_root_filesystem: bool | None = Field(None, alias="readOnlyRootFilesystem")
    run_as_group: int | None = Field(None, alias="runAsGroup")
    run_as_non_root: bool | None = Field(None, alias="runAsNonRoot")
    run_as_user: int | None = Field(None, alias="runAsUser")
    se_linux_options: SELinuxOptions | None = Field(None, alias="seLinuxOptions")
    seccomp_profile: SeccompProfile | None = Field(None, alias="seccompProfile")
    windows_options: WindowsSecurityContextOptions | None = Field(None, alias="windowsOptions")


class ServiceSpec(DataClassDictMixin):
    """Represents the specification of a Kubernetes service."""

    allocate_load_balancer_node_ports: bool | None = Field(None, alias="allocateLoadBalancerNodePorts")
    cluster_ip: str | None = Field(None, alias="clusterIP")
    cluster_i_ps: list[str] | None = Field(None, alias="clusterIPs")
    external_i_ps: list[str] | None = Field(None, alias="externalIPs")
    external_name: str | None = Field(None, alias="externalName")
    external_traffic_policy: str | None = Field(None, alias="externalTrafficPolicy")
    health_check_node_port: int | None = Field(None, alias="healthCheckNodePort")
    internal_traffic_policy: str | None = Field(None, alias="internalTrafficPolicy")
    ip_families: list[str] | None = Field(None, alias="ipFamilies")
    ip_family_policy: str | None = Field(None, alias="ipFamilyPolicy")
    load_balancer_class: str | None = Field(None, alias="loadBalancerClass")
    load_balancer_ip: str | None = Field(None, alias="loadBalancerIP")
    load_balancer_source_ranges: list[str] | None = Field(None, alias="loadBalancerSourceRanges")
    ports: list[ServicePort] | None = Field(None)
    publish_not_ready_addresses: bool | None = Field(None, alias="publishNotReadyAddresses")
    selector: dict[str, str] | None = Field(None)
    session_affinity: str | None = Field(None, alias="sessionAffinity")
    session_affinity_config: SessionAffinityConfig | None = Field(None, alias="sessionAffinityConfig")
    traffic_distribution: str | None = Field(None, alias="trafficDistribution")
    type: str | None = Field(None)


class ServiceStatus(DataClassDictMixin):
    """Represents the status of a Kubernetes service."""

    conditions: list[Condition] | None = Field(None)
    load_balancer: LoadBalancerStatus | None = Field(None, alias="loadBalancer")


class EnvVar(DataClassDictMixin):
    """Represents an environment variable."""

    name: str | None = Field(None)
    value: str | None = Field(None)
    value_from: EnvVarSource | None = Field(None, alias="valueFrom")


class Lifecycle(DataClassDictMixin):
    """Represents lifecycle hooks for a container."""

    post_start: LifecycleHandler | None = Field(None, alias="postStart")
    pre_stop: LifecycleHandler | None = Field(None, alias="preStop")


class ResourceQuotaSpec(DataClassDictMixin):
    """Represents the specification of a resource quota."""

    hard: ResourceList | None = None
    scope_selector: ScopeSelector | None = Field(None, alias="scopeSelector")
    scopes: list[str] | None = Field(None)


class Service(DataClassDictMixin):
    """Represents a Kubernetes service."""

    annotations: dict[str, str] | None = Field(None)
    api_version: str | None = Field(None, alias="apiVersion")
    creation_timestamp: str | None = Field(None, alias="creationTimestamp")
    deletion_grace_period_seconds: int | None = Field(None, alias="deletionGracePeriodSeconds")
    deletion_timestamp: str | None = Field(None, alias="deletionTimestamp")
    finalizers: list[str] | None = Field(None)
    generate_name: str | None = Field(None, alias="generateName")
    generation: int | None = Field(None)
    kind: str | None = Field(None)
    labels: dict[str, str] | None = Field(None)
    managed_fields: list[ManagedFieldsEntry] | None = Field(None, alias="managedFields")
    name: str | None = Field(None)
    namespace: str | None = Field(None)
    owner_references: list[OwnerReference] | None = Field(None, alias="ownerReferences")
    resource_version: str | None = Field(None, alias="resourceVersion")
    self_link: str | None = Field(None, alias="selfLink")
    spec: ServiceSpec | None = None
    status: ServiceStatus | None = None
    uid: str | None = Field(None)


class Container(DataClassDictMixin):
    """Represents a container in a pod."""

    args: list[str] | None = Field(None)
    command: list[str] | None = Field(None)
    env: list[EnvVar] | None = Field(None)
    env_from: list[EnvFromSource] | None = Field(None, alias="envFrom")
    image: str | None = Field(None)
    image_pull_policy: str | None = Field(None, alias="imagePullPolicy")
    lifecycle: Lifecycle | None = None
    liveness_probe: Probe | None = Field(None, alias="livenessProbe")
    name: str | None = Field(None)
    ports: list[ContainerPort] | None = Field(None)
    readiness_probe: Probe | None = Field(None, alias="readinessProbe")
    resize_policy: list[ContainerResizePolicy] | None = Field(None, alias="resizePolicy")
    resources: ResourceRequirements | None = None
    restart_policy: str | None = Field(None, alias="restartPolicy")
    security_context: SecurityContext | None = Field(None, alias="securityContext")
    startup_probe: Probe | None = Field(None, alias="startupProbe")
    stdin: bool | None = Field(None)
    stdin_once: bool | None = Field(None, alias="stdinOnce")
    termination_message_path: str | None = Field(None, alias="terminationMessagePath")
    termination_message_policy: str | None = Field(None, alias="terminationMessagePolicy")
    tty: bool | None = Field(None)
    volume_devices: list[VolumeDevice] | None = Field(None, alias="volumeDevices")
    volume_mounts: list[VolumeMount] | None = Field(None, alias="volumeMounts")
    working_dir: str | None = Field(None, alias="workingDir")


class ResourceQuota(DataClassDictMixin):
    """Represents a resource quota in Kubernetes."""

    annotations: dict[str, str] | None = Field(None)
    api_version: str | None = Field(None, alias="apiVersion")
    creation_timestamp: str | None = Field(None, alias="creationTimestamp")
    deletion_grace_period_seconds: int | None = Field(None, alias="deletionGracePeriodSeconds")
    deletion_timestamp: str | None = Field(None, alias="deletionTimestamp")
    finalizers: list[str] | None = Field(None)
    generate_name: str | None = Field(None, alias="generateName")
    generation: int | None = Field(None)
    kind: str | None = Field(None)
    labels: dict[str, str] | None = Field(None)
    managed_fields: list[ManagedFieldsEntry] | None = Field(None, alias="managedFields")
    name: str | None = Field(None)
    namespace: str | None = Field(None)
    owner_references: list[OwnerReference] | None = Field(None, alias="ownerReferences")
    resource_version: str | None = Field(None, alias="resourceVersion")
    self_link: str | None = Field(None, alias="selfLink")
    spec: ResourceQuotaSpec | None = None
    status: ResourceQuotaStatus | None = None
    uid: str | None = Field(None)
