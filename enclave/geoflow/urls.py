from django.urls import path

from .views import (
    GeoFlowDashboardView,
    GeoFlowLoginView,
    GeoFlowMapsView,
    CustomerListView,
    CustomerCreateView,
    CustomerDetailView,
    ProductListView,
    TransportCreateView,
)

app_name = "geoflow"

urlpatterns = [
    path("login/", GeoFlowLoginView.as_view(), name="login"),
    path("", GeoFlowDashboardView.as_view(), name="dashboard"),
    path("maps/", GeoFlowMapsView.as_view(), name="maps"),
    path("customers/", CustomerListView.as_view(), name="customers"),
    path("customers/new/", CustomerCreateView.as_view(), name="customer_create"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer_detail"),
    path("products/", ProductListView.as_view(), name="products"),
    path("transport/new/", TransportCreateView.as_view(), name="transport_create"),
]
