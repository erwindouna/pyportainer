"""Data models for authentication-related payloads and responses."""

from __future__ import annotations

from mashumaro import DataClassDictMixin
from pydantic import Field


class AuthenticatePayload(DataClassDictMixin):
    """Payload for user authentication."""

    password: str = Field(...)
    username: str = Field(...)


class AuthenticateResponse(DataClassDictMixin):
    """Response containing the JWT token."""

    jwt: str | None = Field(None)


class OauthPayload(DataClassDictMixin):
    """Payload for OAuth authentication."""

    code: str | None = Field(None)


class AuthPayload(DataClassDictMixin):
    """Payload for authentication with optional token."""

    token: str | None = Field(default=None, alias="token")
