from django.views.generic import TemplateView


class GeoFlowLoginView(TemplateView):
    template_name = "geoflow/login.html"


class GeoFlowDashboardView(TemplateView):
    template_name = "geoflow/dashboard.html"


class GeoFlowMapsView(TemplateView):
    template_name = "geoflow/maps.html"


class CustomerListView(TemplateView):
    template_name = "geoflow/customer_list.html"


class CustomerCreateView(TemplateView):
    template_name = "geoflow/customer_form.html"


class CustomerDetailView(TemplateView):
    template_name = "geoflow/customer_detail.html"


class ProductListView(TemplateView):
    template_name = "geoflow/product_list.html"


class TransportCreateView(TemplateView):
    template_name = "geoflow/transport_form.html"
