from rest_framework import serializers

from enclave.geoflow.models import Product, Customer, TransportActivity


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "sku", "description", "created_at")


class CustomerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Product.objects.all(), required=False
    )

    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "address_line1",
            "address_line2",
            "city",
            "region",
            "postal_code",
            "country",
            "latitude",
            "longitude",
            "products",
            "product_ids",
            "uses_transport",
            "created_at",
        )

    def create(self, validated_data):
        product_ids = validated_data.pop("product_ids", [])
        customer = super().create(validated_data)
        if product_ids:
            customer.products.set(product_ids)
        return customer

    def update(self, instance, validated_data):
        product_ids = validated_data.pop("product_ids", None)
        instance = super().update(instance, validated_data)
        if product_ids is not None:
            instance.products.set(product_ids)
        return instance


class TransportActivitySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    customers = CustomerSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Product.objects.all(), required=False
    )
    customer_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Customer.objects.all(), required=False
    )

    class Meta:
        model = TransportActivity
        fields = (
            "id",
            "vehicle_identifier",
            "route",
            "products",
            "product_ids",
            "customers",
            "customer_ids",
            "timestamp",
            "distance_km",
            "duration_minutes",
            "created_at",
        )

    def create(self, validated_data):
        product_ids = validated_data.pop("product_ids", [])
        customer_ids = validated_data.pop("customer_ids", [])
        activity = super().create(validated_data)
        if product_ids:
            activity.products.set(product_ids)
        if customer_ids:
            activity.customers.set(customer_ids)
        return activity

    def update(self, instance, validated_data):
        product_ids = validated_data.pop("product_ids", None)
        customer_ids = validated_data.pop("customer_ids", None)
        instance = super().update(instance, validated_data)
        if product_ids is not None:
            instance.products.set(product_ids)
        if customer_ids is not None:
            instance.customers.set(customer_ids)
        return instance
