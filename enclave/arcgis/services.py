"""Lightweight ArcGIS Python SDK integration wrapper.

This module provides a small runtime-safe wrapper around the ArcGIS
Python SDK. The project does not require the SDK at import time; if
`arcgis` is not installed the wrapper raises a clear error message.

Installation notes are in `enclave/arcgis/README.md` and `pyproject.toml`.
"""
from __future__ import annotations

import os
from typing import Optional


class ArcGISNotInstalled(RuntimeError):
    pass


class ArcGISClient:
    """Minimal helper to obtain an authenticated `GIS` instance.

    Usage:
      client = ArcGISClient()  # reads env vars and connects
      gis = client.gis

    Environment variables supported (attempted in order):
      - ARCGIS_CLIENT_ID / ARCGIS_CLIENT_SECRET (OAuth credentials)
      - ARCGIS_USERNAME / ARCGIS_PASSWORD (user auth against arcgis.com)
      - If none provided, an anonymous connection is created.
    """

    def __init__(self) -> None:
        try:
            from arcgis.gis import GIS  # type: ignore
        except Exception as exc:  # pragma: no cover - import-time behavior
            raise ArcGISNotInstalled(
                "ArcGIS Python SDK not installed. See enclave/arcgis/README.md for install instructions."
            ) from exc

        client_id = os.getenv("ARCGIS_CLIENT_ID")
        client_secret = os.getenv("ARCGIS_CLIENT_SECRET")
        username = os.getenv("ARCGIS_USERNAME")
        password = os.getenv("ARCGIS_PASSWORD")
        portal = os.getenv("ARCGIS_PORTAL_URL", "https://www.arcgis.com")

        # Prefer OAuth client id/secret if available
        if client_id and client_secret:
            # ArcGIS Python SDK supports OAuth workflows; the exact flow
            # may require additional setup. Attempt a token-based connection
            # using portal URL and client credentials where supported.
            try:
                self.gis = GIS(portal, client_id=client_id, client_secret=client_secret)  # type: ignore[call-arg]
                return
            except Exception:
                pass

        # Fallback to username/password if present
        if username and password:
            self.gis = GIS(portal, username, password)  # type: ignore[call-arg]
            return

        # Anonymous connection
        self.gis = GIS(portal)

    gis: Optional[object]

    def info(self) -> dict:
        """Return a small dict with connection info for diagnostics."""
        if not getattr(self, "gis", None):
            return {"connected": False}
        try:
            return {"connected": True, "portal": getattr(self.gis, "url", None)}
        except Exception:
            return {"connected": False}
