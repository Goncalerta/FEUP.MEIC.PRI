"""booksearch api URL Configuration"""

from rest_framework import routers
from django.urls import include, path

from src.booksearch.views import BookViewSet, ExampleViewSet, CategoriesViewSet

router = routers.DefaultRouter()
router.register(r"example", ExampleViewSet, basename="example")
router.register(r"search", BookViewSet, basename="search")
router.register(r"categories", CategoriesViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
]
