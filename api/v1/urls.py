from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.schema import schema_view
from api.v1.views import VPSViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"vps", VPSViewSet, basename="vps")
urlpatterns = [
    path("", include(router.urls)),
    path("docs/", schema_view.with_ui("swagger"), name="swagger"),
]
