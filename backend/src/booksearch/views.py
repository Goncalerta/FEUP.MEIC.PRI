"""booksearch views Configuration"""

from rest_framework import viewsets
from rest_framework.response import Response
from src.booksearch.solr_api import make_query, get_categories


class ExampleViewSet(viewsets.ViewSet):
    """
    Example to implement our api that connects to solr
    """

    def list(self, request):
        # We can do anything in this function, and then return an array [] or object {} or even string ""
        # That will be converted to json
        return Response([{"message": "Hello, world!"}])

    def retrieve(self, request, pk=None):
        # The function "list" was for the GET request of a list (so a search query for example)
        # The function "retrieve" is for the GET request with a  specific primary key (so a specific book for example)
        return Response({"message": "Hello, world!"})


class BookViewSet(viewsets.ViewSet):
    """
    Viewset for searching books.
    """

    def list(self, request):
        data = request.data
        value = data.get("value", "*")
        # import requests
        # from requests.adapters import HTTPAdapter, Retry
        # s = requests.Session()

        # retries = Retry(total=5,
        #         backoff_factor=0.1,
        #         status_forcelist=[ 500, 502, 503, 504 ])
        # s.mount('http://', HTTPAdapter(max_retries=retries))
        # print(s.get(f"http://127.0.0.1:8983"))
        # return Response("lol")
        # return Response(requests.get(f"http://127.0.0.1:8983").json())
        return Response(make_query(q=f"*:{value}", rows=10, start=0))

    def retrieve(self, request, pk=None):
        return Response(make_query(q=f"id:{pk}", rows=10, start=0))

class CategoriesViewSet(viewsets.ViewSet):
    """
    Viewset for enumerating categories.
    """

    def list(self, _request):
        return Response(get_categories())
