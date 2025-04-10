"""Data models for Helm chart operations in Portainer."""

from __future__ import annotations

from mashumaro import DataClassDictMixin


class InstallChartPayload(DataClassDictMixin):
    """Payload for installing a Helm chart."""

    chart: str | None = None
    name: str | None = None
    namespace: str | None = None
    repo: str | None = None
    values: str | None = None
