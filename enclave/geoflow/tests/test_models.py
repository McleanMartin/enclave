import pytest

from enclave.geoflow.models import Product, Customer, TransportActivity


@pytest.mark.django_db
def test_create_product():
    p = Product.objects.create(name="Test Product", sku="TP-001")
    assert p.pk is not None
    assert p.name == "Test Product"


@pytest.mark.django_db
def test_customer_products_relation():
    p1 = Product.objects.create(name="P1")
    p2 = Product.objects.create(name="P2")
    c = Customer.objects.create(name="C1", city="Testville")
    c.products.add(p1, p2)
    assert c.products.count() == 2
    names = {p.name for p in c.products.all()}
    assert names == {"P1", "P2"}
    assert c.latitude is None and c.longitude is None


@pytest.mark.django_db
def test_transport_activity_create_and_relations():
    p = Product.objects.create(name="TP")
    c = Customer.objects.create(name="CustomerX")
    ta = TransportActivity.objects.create(vehicle_identifier="V100", distance_km=12.5, duration_minutes=30)
    ta.products.add(p)
    ta.customers.add(c)
    assert ta.products.count() == 1
    assert ta.customers.count() == 1
    assert ta.vehicle_identifier == "V100"
    assert ta.distance_km == 12.5
