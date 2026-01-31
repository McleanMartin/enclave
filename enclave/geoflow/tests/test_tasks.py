import pytest

from enclave.geoflow.models import Customer


@pytest.mark.django_db
def test_geocode_customer_task(monkeypatch):
    # Create a customer with an address
    c = Customer.objects.create(name="GeoCustomer", address_line1="1 Main St", city="Testville", country="Testland")

    # Create a fake ArcGISClient with expected behavior
    class DummyGIS:
        def geocode(self, address):
            return [{"location": {"x": 30.123456, "y": -20.654321}}]

    class DummyClient:
        def __init__(self):
            self.gis = DummyGIS()

    monkeypatch.setattr("enclave.arcgis.services.ArcGISClient", DummyClient)

    # Import the task here so the patch is active
    from enclave.geoflow.tasks import geocode_customer

    result = geocode_customer(c.id)
    assert result.get("ok") is True
    assert "lat" in result and "lon" in result
    c.refresh_from_db()
    assert c.latitude is not None and c.longitude is not None
