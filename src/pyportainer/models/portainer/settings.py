"""Data models for settings management in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class Edge(DataClassDictMixin):
    """Represents edge agent settings."""

    command_interval: int | None = Field(None, alias="CommandInterval")
    ping_interval: int | None = Field(None, alias="PingInterval")
    snapshot_interval: int | None = Field(None, alias="SnapshotInterval")
    checkin_interval: int | None = Field(None, alias="checkinInterval")


class PublicSettingsResponse(DataClassDictMixin):
    """Response containing public settings."""

    authentication_method: int | None = Field(None, alias="AuthenticationMethod")
    enable_edge_compute_features: bool | None = Field(None, alias="EnableEdgeComputeFeatures")
    enable_telemetry: bool | None = Field(None, alias="EnableTelemetry")
    features: dict[str, bool] | None = Field(None, alias="Features")
    global_deployment_options: portainer.GlobalDeploymentOptions | None = Field(None, alias="GlobalDeploymentOptions")
    is_docker_desktop_extension: bool | None = Field(None, alias="IsDockerDesktopExtension")
    logo_url: str | None = Field(None, alias="LogoURL")
    o_auth_login_uri: str | None = Field(None, alias="OAuthLoginURI")
    o_auth_logout_uri: str | None = Field(None, alias="OAuthLogoutURI")
    required_password_length: int | None = Field(None, alias="RequiredPasswordLength")
    team_sync: bool | None = Field(None, alias="TeamSync")
    edge: Edge | None = None
    is_amt_enabled: bool | None = Field(None, alias="isAMTEnabled")
    kubeconfig_expiry: str | None = Field("0", alias="kubeconfigExpiry")


class SettingsUpdatePayload(DataClassDictMixin):
    """Payload for updating settings."""

    edge_portainer_url: str | None = Field(None, alias="EdgePortainerURL")
    authentication_method: int | None = Field(None, alias="authenticationMethod")
    black_listed_labels: list[portainer.Pair] | None = Field(None, alias="blackListedLabels")
    edge_agent_checkin_interval: int | None = Field(None, alias="edgeAgentCheckinInterval")
    enable_edge_compute_features: bool | None = Field(None, alias="enableEdgeComputeFeatures")
    enable_telemetry: bool | None = Field(None, alias="enableTelemetry")
    enforce_edge_id: bool | None = Field(None, alias="enforceEdgeID")
    global_deployment_options: portainer.GlobalDeploymentOptions | None = Field(None, alias="globalDeploymentOptions")
    helm_repository_url: str | None = Field(None, alias="helmRepositoryURL")
    internal_auth_settings: portainer.InternalAuthSettings | None = Field(None, alias="internalAuthSettings")
    kubeconfig_expiry: str | None = Field("0", alias="kubeconfigExpiry")
    kubectl_shell_image: str | None = Field(None, alias="kubectlShellImage")
    ldapsettings: portainer.LDAPSettings | None = None
    logo_url: str | None = Field(None, alias="logoURL")
    oauth_settings: portainer.OAuthSettings | None = Field(None, alias="oauthSettings")
    snapshot_interval: str | None = Field(None, alias="snapshotInterval")
    templates_url: str | None = Field(None, alias="templatesURL")
    trust_on_first_connect: bool | None = Field(None, alias="trustOnFirstConnect")
    user_session_timeout: str | None = Field(None, alias="userSessionTimeout")
