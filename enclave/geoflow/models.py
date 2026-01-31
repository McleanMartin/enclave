from __future__ import annotations

from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:  # pragma: no cover - display helper
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=128, blank=True)
    region = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=128, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True, related_name="interested_customers")
    uses_transport = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:  # pragma: no cover - display helper
        return self.name


class TransportActivity(models.Model):
    vehicle_identifier = models.CharField(max_length=128)
    # route stored as GeoJSON-like list of coordinates or simple JSON payload
    route = models.JSONField(blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True, related_name="transport_activities")
    customers = models.ManyToManyField(Customer, blank=True, related_name="transport_activities")
    timestamp = models.DateTimeField(default=timezone.now)
    distance_km = models.FloatField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self) -> str:  # pragma: no cover - display helper
        return f"{self.vehicle_identifier} @ {self.timestamp.isoformat()}"
