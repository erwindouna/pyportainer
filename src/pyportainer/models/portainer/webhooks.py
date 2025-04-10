"""Data models for Webhooks in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import BaseModel, Field


class WebhookCreatePayload(DataClassDictMixin, BaseModel):
    """Payload for creating a Portainer webhook."""

    endpoint_id: int | None = Field(
        default=None,
        alias="endpointID",
        json_schema_extra={"example": 1},
    )
    registry_id: int | None = Field(default=None, alias="registryID", json_schema_extra={"example": 1})
    resource_id: str | None = Field(default=None, alias="resourceID")
    webhook_type: int | None = Field(default=None, alias="webhookType")


class WebhookUpdatePayload(DataClassDictMixin, BaseModel):
    """Payload for updating a Portainer webhook."""

    registry_id: int | None = Field(default=None, alias="registryID")


class Webhook(DataClassDictMixin):
    """Represents a Portainer webhook."""

    id: str | None = Field(default=None)
    name: str | None = Field(default=None)
    resource_id: str | None = Field(default=None, alias="resourceId")
    resource_type: str | None = Field(default=None, alias="resourceType")
    token: str | None = Field(default=None)


class WebhookList(DataClassDictMixin):
    """List of Portainer webhooks."""

    webhooks: list[Webhook] | None = Field(default=None)


class WebhookPayload(DataClassDictMixin):
    """Payload for webhook operations."""

    id: int | None = Field(default=None, alias="id")
    name: str | None = Field(default=None, alias="name")
