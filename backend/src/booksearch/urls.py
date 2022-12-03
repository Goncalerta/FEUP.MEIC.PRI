"""booksearch api URL Configuration"""

from rest_framework import routers
from django.urls import include, path

from src.booksearch.views import (
    UserViewSet,
    WorkstationViewSet,
)

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"workstation", WorkstationViewSet, basename="workstation")

urlpatterns = [
    path("", include(router.urls)),
    # path("generate/<int:number_days>", ScheduleViewSet.as_view({"post": "create"})),
]
