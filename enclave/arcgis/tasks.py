from __future__ import annotations

from celery import shared_task

from .services import ArcGISClient, ArcGISNotInstalled


@shared_task()
def check_arcgis_connectivity() -> dict:
    """Celery task that attempts to instantiate the ArcGIS client and
    returns a tiny diagnostic payload. Useful as a health check.
    """
    try:
        client = ArcGISClient()
    except ArcGISNotInstalled:
        return {"ok": False, "reason": "arcgis-sdk-not-installed"}

    try:
        info = client.info()
        return {"ok": info.get("connected", False), "info": info}
    except Exception as exc:
        return {"ok": False, "reason": str(exc)}
