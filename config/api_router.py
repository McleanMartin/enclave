from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from enclave.users.api.views import UserViewSet
from enclave.geoflow.api.views import (
	ProductViewSet,
	CustomerViewSet,
	TransportActivityViewSet,
)

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("products", ProductViewSet)
router.register("customers", CustomerViewSet)
router.register("transport-activities", TransportActivityViewSet)


app_name = "api"
urlpatterns = router.urls
