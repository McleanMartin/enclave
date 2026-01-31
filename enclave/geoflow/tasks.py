from __future__ import annotations

from celery import shared_task

from django.db import transaction

from enclave.arcgis.services import ArcGISClient, ArcGISNotInstalled
from .models import Customer


@shared_task(bind=True)
def geocode_customer(self, customer_id: int) -> dict:
    """Geocode a customer address using the ArcGIS integration.

    This task attempts to use the ArcGIS Python SDK if available; it fails
    gracefully when the SDK is not installed.
    """
    try:
        client = ArcGISClient()
    except ArcGISNotInstalled:
        return {"ok": False, "reason": "arcgis-not-installed"}

    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return {"ok": False, "reason": "customer-not-found"}

    address_parts = [
        customer.address_line1,
        customer.address_line2,
        customer.city,
        customer.region,
        customer.postal_code,
        customer.country,
    ]
    address = ", ".join([p for p in address_parts if p])

    try:
        # Try arcgis.geocoding.geocode first
        results = []
        try:
            from arcgis.geocoding import geocode as arcgis_geocode  # type: ignore

            results = arcgis_geocode(address)
        except Exception:
            try:
                results = client.gis.geocode(address)
            except Exception:
                results = []

        if not results:
            return {"ok": False, "reason": "no-results"}

        top = results[0]
        loc = None
        if isinstance(top, dict):
            loc = top.get("location") or top.get("attributes")

        # common location shape: {'x': lon, 'y': lat}
        if isinstance(loc, dict) and "x" in loc and "y" in loc:
            lon = loc.get("x")
            lat = loc.get("y")
            with transaction.atomic():
                customer.latitude = lat
                customer.longitude = lon
                customer.save(update_fields=("latitude", "longitude"))
            return {"ok": True, "lat": float(lat), "lon": float(lon)}

        return {"ok": False, "reason": "unexpected-result-format"}
    except Exception as exc:
        return {"ok": False, "reason": str(exc)}
