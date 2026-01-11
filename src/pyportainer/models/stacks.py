"""Models for Portainer Stacks API."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


class StackStatus(IntEnum):
    """Stack status values."""

    ACTIVE = 1
    INACTIVE = 2


class StackType(IntEnum):
    """Stack type values."""

    SWARM = 1
    COMPOSE = 2
    KUBERNETES = 3


class GitCredentialAuthType(IntEnum):
    """Git credential authentication types."""

    BASIC = 0
    TOKEN = 1


@dataclass
class StackEnvVar(DataClassORJSONMixin):
    """Environment variable for a stack (name/value pair)."""

    name: str | None = None
    value: str | None = None


@dataclass
class StackOption(DataClassORJSONMixin):
    """Stack deployment options."""

    prune: bool | None = None


@dataclass
class AutoUpdateSettings(DataClassORJSONMixin):
    """GitOps auto-update settings for a stack."""

    force_pull_image: bool | None = field(default=None, metadata=field_options(alias="forcePullImage"))
    force_update: bool | None = field(default=None, metadata=field_options(alias="forceUpdate"))
    interval: str | None = None
    job_id: str | None = field(default=None, metadata=field_options(alias="jobID"))
    webhook: str | None = None


@dataclass
class GitAuthentication(DataClassORJSONMixin):
    """Git authentication configuration."""

    authorization_type: GitCredentialAuthType | None = field(default=None, metadata=field_options(alias="authorizationType"))
    git_credential_id: int | None = field(default=None, metadata=field_options(alias="gitCredentialID"))
    password: str | None = None
    username: str | None = None


@dataclass
class GitRepoConfig(DataClassORJSONMixin):
    """Git repository configuration for a stack."""

    authentication: GitAuthentication | None = None
    config_file_path: str | None = field(default=None, metadata=field_options(alias="configFilePath"))
    config_hash: str | None = field(default=None, metadata=field_options(alias="configHash"))
    reference_name: str | None = field(default=None, metadata=field_options(alias="referenceName"))
    tls_skip_verify: bool | None = field(default=None, metadata=field_options(alias="tlsskipVerify"))
    url: str | None = None


@dataclass
class UserResourceAccess(DataClassORJSONMixin):
    """User access level for a resource."""

    access_level: int | None = field(default=None, metadata=field_options(alias="AccessLevel"))
    user_id: int | None = field(default=None, metadata=field_options(alias="UserId"))


@dataclass
class TeamResourceAccess(DataClassORJSONMixin):
    """Team access level for a resource."""

    access_level: int | None = field(default=None, metadata=field_options(alias="AccessLevel"))
    team_id: int | None = field(default=None, metadata=field_options(alias="TeamId"))


@dataclass
class ResourceControl(DataClassORJSONMixin):
    """Resource access control configuration."""

    id: int | None = field(default=None, metadata=field_options(alias="Id"))
    resource_id: str | None = field(default=None, metadata=field_options(alias="ResourceId"))
    sub_resource_ids: list[str] | None = field(default=None, metadata=field_options(alias="SubResourceIds"))
    type: int | None = field(default=None, metadata=field_options(alias="Type"))
    user_accesses: list[UserResourceAccess] | None = field(default=None, metadata=field_options(alias="UserAccesses"))
    team_accesses: list[TeamResourceAccess] | None = field(default=None, metadata=field_options(alias="TeamAccesses"))
    public: bool | None = field(default=None, metadata=field_options(alias="Public"))
    administrators_only: bool | None = field(default=None, metadata=field_options(alias="AdministratorsOnly"))
    system: bool | None = field(default=None, metadata=field_options(alias="System"))
    owner_id: int | None = field(default=None, metadata=field_options(alias="OwnerId"))


@dataclass
class Stack(DataClassORJSONMixin):
    """Represents a Portainer stack."""

    id: int = field(metadata=field_options(alias="Id"))
    name: str = field(metadata=field_options(alias="Name"))
    type: int = field(metadata=field_options(alias="Type"))
    endpoint_id: int = field(metadata=field_options(alias="EndpointId"))
    status: int = field(metadata=field_options(alias="Status"))

    # Optional fields
    swarm_id: str | None = field(default=None, metadata=field_options(alias="SwarmId"))
    entry_point: str | None = field(default=None, metadata=field_options(alias="EntryPoint"))
    additional_files: list[str] | None = field(default=None, metadata=field_options(alias="AdditionalFiles"))
    env: list[StackEnvVar] | None = field(default=None, metadata=field_options(alias="Env"))
    option: StackOption | None = field(default=None, metadata=field_options(alias="Option"))
    auto_update: AutoUpdateSettings | None = field(default=None, metadata=field_options(alias="AutoUpdate"))
    git_config: GitRepoConfig | None = field(default=None, metadata=field_options(alias="GitConfig"))
    resource_control: ResourceControl | None = field(default=None, metadata=field_options(alias="ResourceControl"))
    project_path: str | None = field(default=None, metadata=field_options(alias="ProjectPath"))
    namespace: str | None = field(default=None, metadata=field_options(alias="Namespace"))
    created_by: str | None = field(default=None, metadata=field_options(alias="CreatedBy"))
    creation_date: int | None = field(default=None, metadata=field_options(alias="CreationDate"))
    updated_by: str | None = field(default=None, metadata=field_options(alias="UpdatedBy"))
    update_date: int | None = field(default=None, metadata=field_options(alias="UpdateDate"))
    from_app_template: bool | None = field(default=None, metadata=field_options(alias="FromAppTemplate"))

    @property
    def is_active(self) -> bool:
        """Check if the stack is active."""
        return self.status == StackStatus.ACTIVE

    @property
    def stack_type(self) -> StackType:
        """Get the stack type as an enum."""
        return StackType(self.type)
