"""Data models for build and runtime information."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class BuildInfo(DataClassDictMixin):
    """Information about the build environment."""

    build_number: str | None = Field(None, alias="buildNumber")
    git_commit: str | None = Field(None, alias="gitCommit")
    go_version: str | None = Field(None, alias="goVersion")
    image_tag: str | None = Field(None, alias="imageTag")
    nodejs_version: str | None = Field(None, alias="nodejsVersion")
    webpack_version: str | None = Field(None, alias="webpackVersion")
    yarn_version: str | None = Field(None, alias="yarnVersion")


class DependenciesInfo(DataClassDictMixin):
    """Information about software dependencies."""

    compose_version: str | None = Field(None, alias="composeVersion")
    docker_version: str | None = Field(None, alias="dockerVersion")
    helm_version: str | None = Field(None, alias="helmVersion")
    kubectl_version: str | None = Field(None, alias="kubectlVersion")


class RuntimeInfo(DataClassDictMixin):
    """Information about the runtime environment."""

    env: list[str] | None = None
