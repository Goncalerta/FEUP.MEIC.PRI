"""booksearch api URL Configuration"""

from rest_framework import routers
from django.urls import include, path

from src.booksearch.views import BookViewSet, SearchViewSet, BrowseViewSet, CategoriesViewSet, MoreLikeThisViewSet, AdvancedSearchViewSet, ExactSearchViewSet

router = routers.DefaultRouter()
router.register(r"search", SearchViewSet, basename="search")
router.register(r"advancedSearch", AdvancedSearchViewSet, basename="advancedSearch")
router.register(r"exactSearch", ExactSearchViewSet, basename="advancedSearch")
router.register(r"browse", BrowseViewSet, basename="browse")
router.register(r"categories", CategoriesViewSet, basename="categories")
router.register(r"moreLikeThis", MoreLikeThisViewSet, basename="moreLikeThis")
router.register(r"book", BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
]
