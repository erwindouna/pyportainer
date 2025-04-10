"""Data models for Kubernetes v1beta1 API objects in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import v1


class ContainerMetrics(DataClassDictMixin):
    """Represents metrics for a container."""

    name: str | None = Field(None)
    usage: v1.ResourceList | None = None


class NodeMetrics(DataClassDictMixin):
    """Represents metrics for a Kubernetes node."""

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
    managed_fields: list[v1.ManagedFieldsEntry] | None = Field(None, alias="managedFields")
    name: str | None = Field(None)
    namespace: str | None = Field(None)
    owner_references: list[v1.OwnerReference] | None = Field(None, alias="ownerReferences")
    resource_version: str | None = Field(None, alias="resourceVersion")
    self_link: str | None = Field(None, alias="selfLink")
    timestamp: str | None = Field(None)
    uid: str | None = Field(None)
    usage: v1.ResourceList | None = None
    window: v1.Duration | None = None


class NodeMetricsList(DataClassDictMixin):
    """Represents a list of node metrics."""

    api_version: str | None = Field(None, alias="apiVersion")
    continue_: str | None = Field(None, alias="continue")
    items: list[NodeMetrics] | None = Field(None)
    kind: str | None = Field(None)
    remaining_item_count: int | None = Field(None, alias="remainingItemCount")
    resource_version: str | None = Field(None, alias="resourceVersion")
    self_link: str | None = Field(None, alias="selfLink")


class PodMetrics(DataClassDictMixin):
    """Represents metrics for a Kubernetes pod."""

    annotations: dict[str, str] | None = Field(None)
    api_version: str | None = Field(None, alias="apiVersion")
    containers: list[ContainerMetrics] | None = Field(None)
    creation_timestamp: str | None = Field(None, alias="creationTimestamp")
    deletion_grace_period_seconds: int | None = Field(None, alias="deletionGracePeriodSeconds")
    deletion_timestamp: str | None = Field(None, alias="deletionTimestamp")
    finalizers: list[str] | None = Field(None)
    generate_name: str | None = Field(None, alias="generateName")
    generation: int | None = Field(None)
    kind: str | None = Field(None)
    labels: dict[str, str] | None = Field(None)
    managed_fields: list[v1.ManagedFieldsEntry] | None = Field(None, alias="managedFields")
    name: str | None = Field(None)
    namespace: str | None = Field(None)
    owner_references: list[v1.OwnerReference] | None = Field(None, alias="ownerReferences")
    resource_version: str | None = Field(None, alias="resourceVersion")
    self_link: str | None = Field(None, alias="selfLink")
    timestamp: str | None = Field(None)
    uid: str | None = Field(None)
    window: v1.Duration | None = None


class PodMetricsList(DataClassDictMixin):
    """Represents a list of pod metrics."""

    api_version: str | None = Field(None, alias="apiVersion")
    continue_: str | None = Field(None, alias="continue")
    items: list[PodMetrics] | None = Field(None)
    kind: str | None = Field(None)
    remaining_item_count: int | None = Field(None, alias="remainingItemCount")
    resource_version: str | None = Field(None, alias="resourceVersion")
    self_link: str | None = Field(None, alias="selfLink")
