from django.contrib import admin

from .models import Product, Customer, TransportActivity


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "created_at")
    search_fields = ("name", "sku")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "region", "country", "uses_transport")
    search_fields = ("name", "address_line1", "city")
    list_filter = ("uses_transport", "country")


@admin.register(TransportActivity)
class TransportActivityAdmin(admin.ModelAdmin):
    list_display = ("vehicle_identifier", "timestamp", "distance_km", "duration_minutes")
    search_fields = ("vehicle_identifier",)
    list_filter = ("timestamp",)
