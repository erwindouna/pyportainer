"""Data models for OpenAMT operations in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import portainer


class DeviceActionPayload(DataClassDictMixin):
    """Payload for performing an action on a device."""

    action: str | None = None


class OpenAMTConfigurePayload(DataClassDictMixin):
    """Payload for configuring OpenAMT settings."""

    cert_file_content: str | None = Field(None, alias="certFileContent")
    cert_file_name: str | None = Field(None, alias="certFileName")
    cert_file_password: str | None = Field(None, alias="certFilePassword")
    domain_name: str | None = Field(None, alias="domainName")
    enabled: bool | None = None
    mpspassword: str | None = None
    mpsserver: str | None = None
    mpsuser: str | None = None


class DeviceFeaturesPayload(DataClassDictMixin):
    """Payload for setting device features."""

    features: portainer.OpenAMTDeviceEnabledFeatures | None = None
