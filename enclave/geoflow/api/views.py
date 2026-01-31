from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from enclave.geoflow.models import Product, Customer, TransportActivity
from enclave.geoflow.api.serializers import (
    ProductSerializer,
    CustomerSerializer,
    TransportActivitySerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=["get"])
    def within_bbox(self, request):
        """Optional helper: return customers within a simple bbox query.

        Expects `min_lat,min_lon,max_lat,max_lon` as query params.
        """
        min_lat = request.query_params.get("min_lat")
        min_lon = request.query_params.get("min_lon")
        max_lat = request.query_params.get("max_lat")
        max_lon = request.query_params.get("max_lon")
        if not all([min_lat, min_lon, max_lat, max_lon]):
            return Response({"detail": "missing bbox params"}, status=status.HTTP_400_BAD_REQUEST)

        qs = self.queryset.filter(
            latitude__gte=min_lat, latitude__lte=max_lat, longitude__gte=min_lon, longitude__lte=max_lon
        )
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TransportActivityViewSet(ModelViewSet):
    queryset = TransportActivity.objects.all()
    serializer_class = TransportActivitySerializer
