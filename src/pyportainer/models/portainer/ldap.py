"""Data models for LDAP operations in Portainer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mashumaro import DataClassDictMixin

if TYPE_CHECKING:
    from . import portainer


class CheckPayload(DataClassDictMixin):
    """Payload for checking LDAP settings."""

    ldapsettings: portainer.LDAPSettings | None = None
