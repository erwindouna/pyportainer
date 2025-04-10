"""Data models for user management in Portainer."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class AccessTokenResponse(DataClassDictMixin):
    """Response containing access token details."""

    api_key: portainer.APIKey | None = Field(None, alias="apiKey")
    raw_api_key: str | None = Field(None, alias="rawAPIKey")


class AddHelmRepoUrlPayload(DataClassDictMixin):
    """Payload for adding a Helm repository URL."""

    url: str | None = None


class AdminInitPayload(DataClassDictMixin):
    """Payload for initializing the admin user."""

    password: str = Field(...)
    username: str = Field(...)


class HelmUserRepositoryResponse(DataClassDictMixin):
    """Response containing Helm user repository details."""

    global_repository: str | None = Field(None, alias="GlobalRepository")
    user_repositories: list[portainer.HelmUserRepository] | None = Field(None, alias="UserRepositories")


class Color(Enum):
    """Enum representing UI color themes."""

    dark = "dark"  # pylint: disable=C0103
    light = "light"  # pylint: disable=C0103
    highcontrast = "highcontrast"  # pylint: disable=C0103
    auto = "auto"  # pylint: disable=C0103


class ThemePayload(DataClassDictMixin):
    """Payload for setting the UI theme."""

    color: Color | None = Field(None)


class UserAccessTokenCreatePayload(DataClassDictMixin):
    """Payload for creating a user access token."""

    description: str = Field(...)
    password: str = Field(...)


class UserCreatePayload(DataClassDictMixin):
    """Payload for creating a user."""

    password: str = Field(...)
    role: int = Field(...)
    username: str = Field(...)


class UserUpdatePasswordPayload(DataClassDictMixin):
    """Payload for updating a user's password."""

    new_password: str = Field(..., alias="newPassword")
    password: str = Field(...)


class UserUpdatePayload(DataClassDictMixin):
    """Payload for updating a user's details."""

    new_password: str = Field(..., alias="newPassword")
    password: str = Field(...)
    role: int = Field(...)
    theme: ThemePayload | None = None
    use_cache: bool = Field(..., alias="useCache")
    username: str = Field(...)
