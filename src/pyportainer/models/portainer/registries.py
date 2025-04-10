"""Data models for Docker registries in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class RegistryConfigurePayload(DataClassDictMixin):
    """Payload for configuring a Docker registry."""

    authentication: bool = Field(...)
    password: str | None = Field(None)
    region: str | None = Field(None)
    tls: bool | None = Field(None)
    tlscacert_file: list[int] | None = Field(None, alias="tlscacertFile")
    tlscert_file: list[int] | None = Field(None, alias="tlscertFile")
    tlskey_file: list[int] | None = Field(None, alias="tlskeyFile")
    tlsskip_verify: bool | None = Field(None, alias="tlsskipVerify")
    username: str | None = Field(None)


class RegistryCreatePayload(DataClassDictMixin):
    """Payload for creating a Docker registry."""

    authentication: bool = Field(...)
    base_url: str | None = Field(None, alias="baseURL")
    ecr: portainer.EcrData | None = None
    gitlab: portainer.GitlabRegistryData | None = None
    name: str = Field(...)
    password: str | None = Field(None)
    quay: portainer.QuayRegistryData | None = None
    type: int = Field(...)
    url: str = Field(...)
    username: str | None = Field(None)


class RegistryUpdatePayload(DataClassDictMixin):
    """Payload for updating a Docker registry."""

    authentication: bool = Field(...)
    base_url: str | None = Field(None, alias="baseURL")
    ecr: portainer.EcrData | None = None
    name: str = Field(...)
    password: str | None = Field(None)
    quay: portainer.QuayRegistryData | None = None
    registry_accesses: portainer.RegistryAccesses | None = Field(None, alias="registryAccesses")
    url: str = Field(...)
    username: str | None = Field(None)
