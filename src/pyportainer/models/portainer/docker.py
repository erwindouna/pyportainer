"""Data models for Docker-related statistics and dashboard responses."""

from __future__ import annotations

from mashumaro import DataClassDictMixin


class ContainerStats(DataClassDictMixin):
    """Statistics about container states."""

    healthy: int | None = None
    running: int | None = None
    stopped: int | None = None
    total: int | None = None
    unhealthy: int | None = None


class ImagesCounters(DataClassDictMixin):
    """Counters for Docker images."""

    size: int | None = None
    total: int | None = None


class DashboardResponse(DataClassDictMixin):
    """Response containing dashboard statistics."""

    containers: ContainerStats | None = None
    images: ImagesCounters | None = None
    networks: int | None = None
    services: int | None = None
    stacks: int | None = None
    volumes: int | None = None
