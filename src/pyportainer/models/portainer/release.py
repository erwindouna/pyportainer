"""Data models for release management in Portainer."""

from __future__ import annotations

from typing import Any

from mashumaro import DataClassDictMixin
from pydantic import Field


class Dependency(DataClassDictMixin):
    """Represents a chart dependency."""

    alias: str | None = Field(None)
    condition: str | None = Field(None)
    enabled: bool | None = Field(None)
    import_values: list[dict[str, Any]] | None = Field(None, alias="import-values")
    name: str | None = Field(None)
    repository: str | None = Field(None)
    tags: list[str] | None = Field(None)
    version: str | None = Field(None)


class File(DataClassDictMixin):
    """Represents a file in a chart archive."""

    data: list[int] | None = Field(None)
    name: str | None = Field(None)


class HookExecution(DataClassDictMixin):
    """Represents the execution details of a hook."""

    completed_at: str | None = Field(None)
    phase: str | None = Field(None)
    started_at: str | None = Field(None)


class Lock(DataClassDictMixin):
    """Represents a lock file for chart dependencies."""

    dependencies: list[Dependency] | None = Field(None)
    digest: str | None = Field(None)
    generated: str | None = Field(None)


class Maintainer(DataClassDictMixin):
    """Represents a chart maintainer."""

    email: str | None = Field(None)
    name: str | None = Field(None)
    url: str | None = Field(None)


class Metadata(DataClassDictMixin):
    """Represents metadata for a chart."""

    annotations: dict[str, str] | None = Field(None)
    api_version: str | None = Field(None, alias="apiVersion")
    app_version: str | None = Field(None, alias="appVersion")
    condition: str | None = Field(None)
    dependencies: list[Dependency] | None = Field(None)
    deprecated: bool | None = Field(None)
    description: str | None = Field(None)
    home: str | None = Field(None)
    icon: str | None = Field(None)
    keywords: list[str] | None = Field(None)
    kube_version: str | None = Field(None, alias="kubeVersion")
    maintainers: list[Maintainer] | None = Field(None)
    name: str | None = Field(None)
    sources: list[str] | None = Field(None)
    tags: str | None = Field(None)
    type: str | None = Field(None)
    version: str | None = Field(None)


class ReleaseElement(DataClassDictMixin):
    """Represents an element of a release."""

    app_version: str | None = None
    chart: str | None = None
    name: str | None = None
    namespace: str | None = None
    revision: str | None = None
    status: str | None = None
    updated: str | None = None


class Chart(DataClassDictMixin):
    """Represents a Helm chart."""

    files: list[File] | None = Field(None)
    lock: Lock | None = None
    metadata: Metadata | None = None
    schema_: list[int] | None = Field(None, alias="schema")
    templates: list[File] | None = Field(None)
    values: dict[str, dict[str, Any]] | None = Field(None)


class Hook(DataClassDictMixin):
    """Represents a Helm hook."""

    delete_policies: list[str] | None = Field(None)
    events: list[str] | None = Field(None)
    kind: str | None = Field(None)
    last_run: HookExecution | None = None
    manifest: str | None = Field(None)
    name: str | None = None
    path: str | None = Field(None)
    weight: int | None = Field(None)


class Release(DataClassDictMixin):
    """Represents a Helm release."""

    chart: Chart | None = None
    config: dict[str, dict[str, Any]] | None = Field(None)
    hooks: list[Hook] | None = Field(None)
    manifest: str | None = Field(None)
    name: str | None = Field(None)
    namespace: str | None = Field(None)
    version: int | None = Field(None)
