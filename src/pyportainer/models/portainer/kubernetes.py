"""Data models for Kubernetes-related operations in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import v1, v2


class Configuration(DataClassDictMixin):
    """Represents a Kubernetes configuration."""

    configuration_owner: str | None = Field(None, alias="ConfigurationOwner")
    data: dict[str, Any] | None = Field(None, alias="Data")
    kind: str | None = Field(None, alias="Kind")


class K8sApplicationResource(DataClassDictMixin):
    """Represents resource limits and requests for a Kubernetes application."""

    cpu_limit: float | None = Field(None, alias="CpuLimit")
    cpu_request: float | None = Field(None, alias="CpuRequest")
    memory_limit: int | None = Field(None, alias="MemoryLimit")
    memory_request: int | None = Field(None, alias="MemoryRequest")


class K8sClusterRole(DataClassDictMixin):
    """Represents a Kubernetes cluster role."""

    creation_date: str | None = Field(None, alias="creationDate")
    is_system: bool | None = Field(None, alias="isSystem")
    name: str | None = None
    uid: str | None = Field(None, alias="uid")


class K8sConfigurationOwnerResource(DataClassDictMixin):
    """Represents a Kubernetes configuration owner resource."""

    id: str | None = Field(None, alias="Id")
    name: str | None = Field(None, alias="Name")
    resource_kind: str | None = Field(None, alias="ResourceKind")


class K8sCronJobDeleteRequests(DataClassDictMixin):
    """Represents delete requests for Kubernetes cron jobs."""

    __root__: dict[str, list[str]] | None = None


class K8sDashboard(DataClassDictMixin):
    """Represents Kubernetes dashboard statistics."""

    applications_count: int | None = Field(None, alias="applicationsCount")
    config_maps_count: int | None = Field(None, alias="configMapsCount")
    ingresses_count: int | None = Field(None, alias="ingressesCount")
    namespaces_count: int | None = Field(None, alias="namespacesCount")
    secrets_count: int | None = Field(None, alias="secretsCount")
    services_count: int | None = Field(None, alias="servicesCount")
    volumes_count: int | None = Field(None, alias="volumesCount")


class K8sIngressController(DataClassDictMixin):
    """Represents a Kubernetes ingress controller."""

    availability: bool | None = Field(None, alias="Availability")
    class_name: str | None = Field(None, alias="ClassName")
    name: str | None = Field(None, alias="Name")
    new: bool | None = Field(None, alias="New")
    type: str | None = Field(None, alias="Type")
    used: bool | None = Field(None, alias="Used")


class K8sIngressDeleteRequests(DataClassDictMixin):
    """Represents delete requests for Kubernetes ingresses."""

    __root__: dict[str, list[str]] | None = None


class K8sIngressPath(DataClassDictMixin):
    """Represents a path in a Kubernetes ingress."""

    has_service: bool | None = Field(None, alias="HasService")
    host: str | None = Field(None, alias="Host")
    ingress_name: str | None = Field(None, alias="IngressName")
    path: str | None = Field(None, alias="Path")
    path_type: str | None = Field(None, alias="PathType")
    port: int | None = Field(None, alias="Port")
    service_name: str | None = Field(None, alias="ServiceName")


class K8sIngressTLS(DataClassDictMixin):
    """Represents TLS information for a Kubernetes ingress."""

    hosts: list[str] | None = Field(None, alias="Hosts")
    secret_name: str | None = Field(None, alias="SecretName")


class K8sJobDeleteRequests(DataClassDictMixin):
    """Represents delete requests for Kubernetes jobs."""

    __root__: dict[str, list[str]] | None = None


class K8sResourceQuota(DataClassDictMixin):
    """Represents resource quotas for a Kubernetes namespace."""

    cpu: str | None = None
    enabled: bool | None = None
    memory: str | None = None


class K8sRole(DataClassDictMixin):
    """Represents a Kubernetes role."""

    creation_date: str | None = Field(None, alias="creationDate")
    is_system: bool | None = Field(None, alias="isSystem")
    name: str | None = None
    namespace: str | None = None
    uid: str | None = Field(None, alias="uid")


class K8sRoleBindingDeleteRequests(DataClassDictMixin):
    """Represents delete requests for Kubernetes role bindings."""

    __root__: dict[str, list[str]] | None = None


class K8sRoleDeleteRequests(DataClassDictMixin):
    """Represents delete requests for Kubernetes roles."""

    __root__: dict[str, list[str]] | None = None


class K8sSecret(DataClassDictMixin):
    """Represents a Kubernetes secret."""

    annotations: dict[str, str] | None = Field(None, alias="Annotations")
    configuration_owner: str | None = Field(None, alias="ConfigurationOwner")
    configuration_owner_id: str | None = Field(None, alias="ConfigurationOwnerId")
    configuration_owners: list[K8sConfigurationOwnerResource] | None = Field(None, alias="ConfigurationOwners")
    creation_date: str | None = Field(None, alias="CreationDate")
    data: dict[str, str] | None = Field(None, alias="Data")
    is_used: bool | None = Field(None, alias="IsUsed")
    labels: dict[str, str] | None = Field(None, alias="Labels")
    name: str | None = Field(None, alias="Name")
    namespace: str | None = Field(None, alias="Namespace")
    secret_type: str | None = Field(None, alias="SecretType")
    uid: str | None = Field(None, alias="UID")


class K8sServiceAccount(DataClassDictMixin):
    """Represents a Kubernetes service account."""

    creation_date: str | None = Field(None, alias="creationDate")
    is_system: bool | None = Field(None, alias="isSystem")
    name: str | None = None
    namespace: str | None = None
    uid: str | None = Field(None, alias="uid")


class K8sServiceAccountDeleteRequests(DataClassDictMixin):
    """Represents delete requests for Kubernetes service accounts."""

    __root__: dict[str, list[str]] | None = None


class K8sServiceDeleteRequests(DataClassDictMixin):
    """Represents delete requests for Kubernetes services."""

    __root__: dict[str, list[str]] | None = None


class K8sServiceIngress(DataClassDictMixin):
    """Represents an ingress status for a Kubernetes service."""

    hostname: str | None = Field(None, alias="Hostname")
    ip: str | None = Field(None, alias="IP")


class K8sServicePort(DataClassDictMixin):
    """Represents a port for a Kubernetes service."""

    name: str | None = Field(None, alias="Name")
    node_port: int | None = Field(None, alias="NodePort")
    port: int | None = Field(None, alias="Port")
    protocol: str | None = Field(None, alias="Protocol")
    target_port: str | None = Field(None, alias="TargetPort")


class K8sStorageClass(DataClassDictMixin):
    """Represents a Kubernetes storage class."""

    allow_volume_expansion: bool | None = Field(None, alias="allowVolumeExpansion")
    name: str | None = None
    provisioner: str | None = None
    reclaim_policy: str | None = Field(None, alias="reclaimPolicy")


class Metadata(DataClassDictMixin):
    """Represents metadata for a Kubernetes application."""

    labels: dict[str, str] | None = None


class Pod(DataClassDictMixin):
    """Represents a Kubernetes pod."""

    status: str | None = Field(None, alias="Status")


class TLSInfo(DataClassDictMixin):
    """Represents TLS information for a Kubernetes application."""

    hosts: list[str] | None = None


class NamespacesToggleSystemPayload(DataClassDictMixin):
    """Payload for toggling system namespaces."""

    system: bool | None = Field(None)


class IngressRule(DataClassDictMixin):
    """Represents an ingress rule for a Kubernetes application."""

    host: str | None = Field(None, alias="Host")
    ip: str | None = Field(None, alias="IP")
    path: str | None = Field(None, alias="Path")
    tls: list[TLSInfo] | None = Field(None, alias="TLS")


class K8sClusterRoleBinding(DataClassDictMixin):
    """Represents a Kubernetes cluster role binding."""

    creation_date: str | None = Field(None, alias="creationDate")
    is_system: bool | None = Field(None, alias="isSystem")
    name: str | None = None
    namespace: str | None = None
    role_ref: v1.RoleRef | None = Field(None, alias="roleRef")
    subjects: list[v1.Subject] | None = None
    uid: str | None = Field(None, alias="uid")


class K8sConfigMap(DataClassDictMixin):
    """Represents a Kubernetes config map."""

    annotations: dict[str, str] | None = Field(None, alias="Annotations")
    configuration_owner: str | None = Field(None, alias="ConfigurationOwner")
    configuration_owner_id: str | None = Field(None, alias="ConfigurationOwnerId")
    configuration_owners: list[K8sConfigurationOwnerResource] | None = Field(None, alias="ConfigurationOwners")
    creation_date: str | None = Field(None, alias="CreationDate")
    data: dict[str, str] | None = Field(None, alias="Data")
    is_used: bool | None = Field(None, alias="IsUsed")
    labels: dict[str, str] | None = Field(None, alias="Labels")
    name: str | None = Field(None, alias="Name")
    namespace: str | None = Field(None, alias="Namespace")
    uid: str | None = Field(None, alias="UID")


class K8sIngressInfo(DataClassDictMixin):
    """Represents information about a Kubernetes ingress."""

    annotations: dict[str, str] | None = Field(None, alias="Annotations")
    class_name: str | None = Field(None, alias="ClassName")
    creation_date: str | None = Field(None, alias="CreationDate")
    hosts: list[str] | None = Field(None, alias="Hosts")
    labels: dict[str, str] | None = Field(None, alias="Labels")
    name: str | None = Field(None, alias="Name")
    namespace: str | None = Field(None, alias="Namespace")
    paths: list[K8sIngressPath] | None = Field(None, alias="Paths")
    tls: list[K8sIngressTLS] | None = Field(None, alias="TLS")
    type: str | None = Field(None, alias="Type")
    uid: str | None = Field(None, alias="UID")


class K8sNamespaceDetails(DataClassDictMixin):
    """Represents details of a Kubernetes namespace."""

    annotations: dict[str, str] | None = Field(None, alias="Annotations")
    name: str | None = Field(None, alias="Name")
    owner: str | None = Field(None, alias="Owner")
    resource_quota: K8sResourceQuota | None = Field(None, alias="ResourceQuota")


class K8sRoleBinding(DataClassDictMixin):
    """Represents a Kubernetes role binding."""

    creation_date: str | None = Field(None, alias="creationDate")
    is_system: bool | None = Field(None, alias="isSystem")
    name: str | None = None
    namespace: str | None = None
    role_ref: v1.RoleRef | None = Field(None, alias="roleRef")
    subjects: list[v1.Subject] | None = None
    uid: str | None = Field(None, alias="uid")


class PublishedPort(DataClassDictMixin):
    """Represents a published port for a Kubernetes application."""

    ingress_rules: list[IngressRule] | None = Field(None, alias="IngressRules")
    port: int | None = Field(None, alias="Port")


class K8sPersistentVolume(DataClassDictMixin):
    """Represents a Kubernetes persistent volume."""

    access_modes: list[str] | None = Field(None, alias="accessModes")
    annotations: dict[str, str] | None = None
    capacity: v1.ResourceList | None = None
    claim_ref: v1.ObjectReference | None = Field(None, alias="claimRef")
    csi: v1.CSIPersistentVolumeSource | None = None
    name: str | None = None
    persistent_volume_reclaim_policy: str | None = Field(None, alias="persistentVolumeReclaimPolicy")
    storage_class_name: str | None = Field(None, alias="storageClassName")
    volume_mode: str | None = Field(None, alias="volumeMode")


class K8sJob(DataClassDictMixin):
    """Represents a Kubernetes job."""

    backoff_limit: int | None = Field(None, alias="BackoffLimit")
    command: str | None = Field(None, alias="Command")
    completions: int | None = Field(None, alias="Completions")
    container: v1.Container | None = Field(None, alias="Container")
    duration: str | None = Field(None, alias="Duration")
    failed_reason: str | None = Field(None, alias="FailedReason")
    finish_time: str | None = Field(None, alias="FinishTime")
    id: str | None = Field(None, alias="Id")
    is_system: bool | None = Field(None, alias="IsSystem")
    name: str | None = Field(None, alias="Name")
    namespace: str | None = Field(None, alias="Namespace")
    pod_name: str | None = Field(None, alias="PodName")
    start_time: str | None = Field(None, alias="StartTime")
    status: str | None = Field(None, alias="Status")


class K8sApplication(DataClassDictMixin):
    """Represents a Kubernetes application."""

    application_owner: str | None = Field(None, alias="ApplicationOwner")
    application_type: str | None = Field(None, alias="ApplicationType")
    configurations: list[Configuration] | None = Field(None, alias="Configurations")
    containers: list[dict[str, Any]] | None = Field(None, alias="Containers")
    creation_date: str | None = Field(None, alias="CreationDate")
    deployment_type: str | None = Field(None, alias="DeploymentType")
    horizontal_pod_autoscaler: v2.HorizontalPodAutoscaler | None = Field(None, alias="HorizontalPodAutoscaler")
    id: str | None = Field(None, alias="Id")
    image: str | None = Field(None, alias="Image")
    kind: str | None = Field(None, alias="Kind")
    labels: dict[str, str] | None = Field(None, alias="Labels")
    load_balancer_ip_address: str | None = Field(None, alias="LoadBalancerIPAddress")
    match_labels: dict[str, str] | None = Field(None, alias="MatchLabels")
    metadata: Metadata | None = Field(None, alias="Metadata")
    name: str | None = Field(None, alias="Name")
    namespace: str | None = Field(None, alias="Namespace")
    pods: list[Pod] | None = Field(None, alias="Pods")
    published_ports: list[PublishedPort] | None = Field(None, alias="PublishedPorts")
    resource: K8sApplicationResource | None = Field(None, alias="Resource")
    resource_pool: str | None = Field(None, alias="ResourcePool")
    running_pods_count: int | None = Field(None, alias="RunningPodsCount")
    service_id: str | None = Field(None, alias="ServiceId")
    service_name: str | None = Field(None, alias="ServiceName")
    service_type: str | None = Field(None, alias="ServiceType")
    services: list[v1.Service] | None = Field(None, alias="Services")
    stack_id: str | None = Field(None, alias="StackId")
    stack_name: str | None = Field(None, alias="StackName")
    status: str | None = Field(None, alias="Status")
    total_pods_count: int | None = Field(None, alias="TotalPodsCount")
    uid: str | None = Field(None, alias="Uid")


class K8sCronJob(DataClassDictMixin):
    """Represents a Kubernetes cron job."""

    command: str | None = Field(None, alias="Command")
    id: str | None = Field(None, alias="Id")
    is_system: bool | None = Field(None, alias="IsSystem")
    jobs: list[K8sJob] | None = Field(None, alias="Jobs")
    name: str | None = Field(None, alias="Name")
    namespace: str | None = Field(None, alias="Namespace")
    schedule: str | None = Field(None, alias="Schedule")
    suspend: bool | None = Field(None, alias="Suspend")
    timezone: str | None = Field(None, alias="Timezone")


class K8sPersistentVolumeClaim(DataClassDictMixin):
    """Represents a Kubernetes persistent volume claim."""

    access_modes: list[str] | None = Field(None, alias="accessModes")
    creation_date: str | None = Field(None, alias="creationDate")
    id: str | None = None
    labels: dict[str, str] | None = None
    name: str | None = None
    namespace: str | None = None
    owning_applications: list[K8sApplication] | None = Field(None, alias="owningApplications")
    phase: str | None = None
    resources_requests: v1.ResourceList | None = Field(None, alias="resourcesRequests")
    storage: int | None = None
    storage_class: str | None = Field(None, alias="storageClass")
    volume_mode: str | None = Field(None, alias="volumeMode")
    volume_name: str | None = Field(None, alias="volumeName")


class K8sServiceInfo(DataClassDictMixin):
    """Represents information about a Kubernetes service."""

    allocate_load_balancer_node_ports: bool | None = Field(None, alias="allocateLoadBalancerNodePorts")
    annotations: dict[str, str] | None = None
    applications: list[K8sApplication] | None = Field(None)
    cluster_i_ps: list[str] | None = Field(None, alias="clusterIPs")
    creation_date: str | None = Field(None, alias="creationDate")
    external_i_ps: list[str] | None = Field(None, alias="externalIPs")
    external_name: str | None = Field(None, alias="externalName")
    ingress_status: list[K8sServiceIngress] | None = Field(None, alias="ingressStatus")
    labels: dict[str, str] | None = None
    name: str | None = None
    namespace: str | None = None
    ports: list[K8sServicePort] | None = None
    selector: dict[str, str] | None = None
    type: str | None = None
    uid: str | None = None


class K8sVolumeInfo(DataClassDictMixin):
    """Represents information about a Kubernetes volume."""

    persistent_volume: K8sPersistentVolume | None = Field(None, alias="persistentVolume")
    persistent_volume_claim: K8sPersistentVolumeClaim | None = Field(None, alias="persistentVolumeClaim")
    storage_class: K8sStorageClass | None = Field(None, alias="storageClass")
