"""Data models for Kubernetes v2 API objects in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin
from pydantic import Field

if TYPE_CHECKING:
    from . import resource as resource_1
    from . import v1


class CrossVersionObjectReference(DataClassDictMixin):
    """Represents a reference to an object across API versions."""

    api_version: str | None = Field(None, alias="apiVersion")
    kind: str | None = Field(None)
    name: str | None = Field(None)


class HPAScalingPolicy(DataClassDictMixin):
    """Defines a scaling policy for the HorizontalPodAutoscaler."""

    period_seconds: int | None = Field(None, alias="periodSeconds")
    type: str | None = Field(None)
    value: int | None = Field(None)


class HPAScalingRules(DataClassDictMixin):
    """Defines scaling rules for the HorizontalPodAutoscaler."""

    policies: list[HPAScalingPolicy] | None = Field(None)
    select_policy: str | None = Field(None, alias="selectPolicy")
    stabilization_window_seconds: int | None = Field(None, alias="stabilizationWindowSeconds")


class HorizontalPodAutoscalerBehavior(DataClassDictMixin):
    """Specifies the behavior of the HorizontalPodAutoscaler."""

    scale_down: HPAScalingRules | None = Field(None, alias="scaleDown")
    scale_up: HPAScalingRules | None = Field(None, alias="scaleUp")


class HorizontalPodAutoscalerCondition(DataClassDictMixin):
    """Represents a condition of the HorizontalPodAutoscaler."""

    last_transition_time: str | None = Field(None, alias="lastTransitionTime")
    message: str | None = Field(None)
    reason: str | None = Field(None)
    status: str | None = Field(None)
    type: str | None = Field(None)


class MetricTarget(DataClassDictMixin):
    """Defines a target for a metric."""

    average_utilization: int | None = Field(None, alias="averageUtilization")
    average_value: resource_1.Quantity | None = Field(None, alias="averageValue")
    type: str | None = Field(None)
    value: resource_1.Quantity | None = None


class MetricValueStatus(DataClassDictMixin):
    """Represents the current value of a metric."""

    average_utilization: int | None = Field(None, alias="averageUtilization")
    average_value: resource_1.Quantity | None = Field(None, alias="averageValue")
    value: resource_1.Quantity | None = None


class ResourceMetricSource(DataClassDictMixin):
    """Defines a source for resource metrics."""

    name: str | None = Field(None)
    target: MetricTarget | None = None


class ResourceMetricStatus(DataClassDictMixin):
    """Represents the current status of resource metrics."""

    current: MetricValueStatus | None = None
    name: str | None = Field(None)


class ContainerResourceMetricSource(DataClassDictMixin):
    """Defines a source for container resource metrics."""

    container: str | None = Field(None)
    name: str | None = Field(None)
    target: MetricTarget | None = None


class ContainerResourceMetricStatus(DataClassDictMixin):
    """Represents the current status of container resource metrics."""

    container: str | None = Field(None)
    current: MetricValueStatus | None = None
    name: str | None = Field(None)


class MetricIdentifier(DataClassDictMixin):
    """Identifies a metric."""

    name: str | None = Field(None)
    selector: v1.LabelSelector | None = None


class ObjectMetricSource(DataClassDictMixin):
    """Defines a source for object metrics."""

    described_object: CrossVersionObjectReference | None = Field(None, alias="describedObject")
    metric: MetricIdentifier | None = None
    target: MetricTarget | None = None


class ObjectMetricStatus(DataClassDictMixin):
    """Represents the current status of object metrics."""

    current: MetricValueStatus | None = None
    described_object: CrossVersionObjectReference | None = Field(None, alias="describedObject")
    metric: MetricIdentifier | None = None


class PodsMetricSource(DataClassDictMixin):
    """Defines a source for pods metrics."""

    metric: MetricIdentifier | None = None
    target: MetricTarget | None = None


class PodsMetricStatus(DataClassDictMixin):
    """Represents the current status of pods metrics."""

    current: MetricValueStatus | None = None
    metric: MetricIdentifier | None = None


class ExternalMetricSource(DataClassDictMixin):
    """Defines a source for external metrics."""

    metric: MetricIdentifier | None = None
    target: MetricTarget | None = None


class ExternalMetricStatus(DataClassDictMixin):
    """Represents the current status of external metrics."""

    current: MetricValueStatus | None = None
    metric: MetricIdentifier | None = None


class MetricSpec(DataClassDictMixin):
    """Defines a specification for metrics."""

    container_resource: ContainerResourceMetricSource | None = Field(None, alias="containerResource")
    external: ExternalMetricSource | None = None
    object: ObjectMetricSource | None = None
    pods: PodsMetricSource | None = None
    resource: ResourceMetricSource | None = None
    type: str | None = Field(None)


class MetricStatus(DataClassDictMixin):
    """Represents the current status of metrics."""

    container_resource: ContainerResourceMetricStatus | None = Field(None, alias="containerResource")
    external: ExternalMetricStatus | None = None
    object: ObjectMetricStatus | None = None
    pods: PodsMetricStatus | None = None
    resource: ResourceMetricStatus | None = None
    type: str | None = Field(None)


class HorizontalPodAutoscalerSpec(DataClassDictMixin):
    """Defines the specification for a HorizontalPodAutoscaler."""

    behavior: HorizontalPodAutoscalerBehavior | None = None
    max_replicas: int | None = Field(None, alias="maxReplicas")
    metrics: list[MetricSpec] | None = Field(None)
    min_replicas: int | None = Field(None, alias="minReplicas")
    scale_target_ref: CrossVersionObjectReference | None = Field(None, alias="scaleTargetRef")


class HorizontalPodAutoscalerStatus(DataClassDictMixin):
    """Represents the current status of a HorizontalPodAutoscaler."""

    conditions: list[HorizontalPodAutoscalerCondition] | None = Field(None)
    current_metrics: list[MetricStatus] | None = Field(None, alias="currentMetrics")
    current_replicas: int | None = Field(None, alias="currentReplicas")
    desired_replicas: int | None = Field(None, alias="desiredReplicas")
    last_scale_time: str | None = Field(None, alias="lastScaleTime")
    observed_generation: int | None = Field(None, alias="observedGeneration")


class HorizontalPodAutoscaler(DataClassDictMixin):
    """Represents a HorizontalPodAutoscaler."""

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
    spec: HorizontalPodAutoscalerSpec | None = None
    status: HorizontalPodAutoscalerStatus | None = None
    uid: str | None = Field(None)
