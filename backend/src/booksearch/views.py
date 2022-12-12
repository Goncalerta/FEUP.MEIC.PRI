"""booksearch views Configuration"""

from rest_framework import viewsets
from rest_framework.response import Response
from src.booksearch.solr_api import make_query_basic, get_categories, get_book


# class ExampleViewSet(viewsets.ViewSet):
#     """
#     Example to implement our api that connects to solr
#     """

#     def list(self, request):
#         # We can do anything in this function, and then return an array [] or object {} or even string ""
#         # That will be converted to json
#         return Response([{"message": "Hello, world!"}])

#     def retrieve(self, request, pk=None):
#         # The function "list" was for the GET request of a list (so a search query for example)
#         # The function "retrieve" is for the GET request with a  specific primary key (so a specific book for example)
#         return Response({"message": "Hello, world!"})


class SearchViewSet(viewsets.ViewSet):
    """
    Viewset for searching books.
    """

    def list(self, request):
        data = request.query_params
        value = data.get("value", "")
        exact = data.get("exact_query", False)
        return Response(make_query_basic(q=value, rows=10, start=0, exact=exact))


class BrowseViewSet(viewsets.ViewSet):
    """
    Viewset for general book browsing.
    """

    def list(self, _request):
        return Response(make_query_basic(rows=10, start=0))


class CategoriesViewSet(viewsets.ViewSet):
    """
    Viewset for enumerating categories.
    """

    def list(self, _request):
        return Response(get_categories())

class BookViewSet(viewsets.ViewSet):
    """
    Viewset for searching books.
    """
    def retrieve(self, _request, pk=None):
        return Response(get_book(pk))
