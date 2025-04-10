"""Data models for Portainer endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class DockerhubStatusResponse(DataClassDictMixin):
    """Response for Dockerhub status with rate limit info."""

    limit: int | None = Field(None)
    remaining: int | None = Field(None)


class EndpointCreateGlobalKeyResponse(DataClassDictMixin):
    """Represents the response for creating a global key for an endpoint."""

    endpoint_id: int | None = Field(None, alias="endpointID")


class EndpointDeleteBatchPartialResponse(DataClassDictMixin):
    """Represents the partial response for batch deletion of endpoints."""

    deleted: list[int] | None = None
    errors: list[int] | None = None


class EndpointDeleteRequest(DataClassDictMixin):
    """Represents a request to delete an endpoint."""

    delete_cluster: bool | None = Field(None, alias="deleteCluster")
    id: int | None = None


class Relations(DataClassDictMixin):
    """Represents relations for an endpoint."""

    edge_groups: list[int] | None = Field(None, alias="edgeGroups")
    group: int | None = Field(None)
    tags: list[int] | None = None


class EndpointUpdateRelationsPayload(DataClassDictMixin):
    """Represents the payload for updating endpoint relations."""

    relations: dict[str, Relations] | None = None


class ForceUpdateServicePayload(DataClassDictMixin):
    """Represents the payload for forcing a service update."""

    pull_image: bool | None = Field(None, alias="pullImage")
    service_id: str | None = Field(None, alias="serviceID")


class EndpointDeleteBatchPayload(DataClassDictMixin):
    """Represents the payload for batch deletion of endpoints."""

    endpoints: list[EndpointDeleteRequest] | None = None


class EndpointSettingsUpdatePayload(DataClassDictMixin):
    """Represents the payload for updating endpoint settings."""

    allow_bind_mounts_for_regular_users: bool | None = Field(None, alias="allowBindMountsForRegularUsers")
    allow_container_capabilities_for_regular_users: bool | None = Field(None, alias="allowContainerCapabilitiesForRegularUsers")
    allow_device_mapping_for_regular_users: bool | None = Field(None, alias="allowDeviceMappingForRegularUsers")
    allow_host_namespace_for_regular_users: bool | None = Field(None, alias="allowHostNamespaceForRegularUsers")
    allow_privileged_mode_for_regular_users: bool | None = Field(None, alias="allowPrivilegedModeForRegularUsers")
    allow_stack_management_for_regular_users: bool | None = Field(None, alias="allowStackManagementForRegularUsers")
    allow_sysctl_setting_for_regular_users: bool | None = Field(None, alias="allowSysctlSettingForRegularUsers")
    allow_volume_browser_for_regular_users: bool | None = Field(None, alias="allowVolumeBrowserForRegularUsers")
    enable_gpu_management: bool | None = Field(None, alias="enableGPUManagement")
    enable_host_management_features: bool | None = Field(None, alias="enableHostManagementFeatures")
    gpus: list[portainer.Pair] | None = None


class RegistryAccessPayload(DataClassDictMixin):
    """Represents the payload for registry access."""

    namespaces: list[str] | None = None
    team_access_policies: portainer.TeamAccessPolicies | None = Field(None, alias="teamAccessPolicies")
    user_access_policies: portainer.UserAccessPolicies | None = Field(None, alias="userAccessPolicies")


class EndpointUpdatePayload(DataClassDictMixin):
    """Represents the payload for updating an endpoint."""

    azure_application_id: str | None = Field(None, alias="azureApplicationID")
    azure_authentication_key: str | None = Field(None, alias="azureAuthenticationKey")
    azure_tenant_id: str | None = Field(None, alias="azureTenantID")
    edge_checkin_interval: int | None = Field(None, alias="edgeCheckinInterval")
    gpus: list[portainer.Pair] | None = None
    group_id: int | None = Field(None, alias="groupID")
    kubernetes: portainer.KubernetesData | None = None
    name: str | None = None
    public_url: str | None = Field(None, alias="publicURL")
    status: int | None = Field(None)
    tag_i_ds: list[int] | None = Field(None, alias="tagIDs")
    team_access_policies: portainer.TeamAccessPolicies | None = Field(None, alias="teamAccessPolicies")
    tls: bool | None = Field(None)
    tlsskip_client_verify: bool | None = Field(None, alias="tlsskipClientVerify")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")
    url: str | None = Field(None)
    user_access_policies: portainer.UserAccessPolicies | None = Field(None, alias="userAccessPolicies")
