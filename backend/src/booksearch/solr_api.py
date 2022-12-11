import requests
import os
from textblob import TextBlob

SOLR_HOST = os.environ.get("SOLR_HOST", "solr")
SOLR_PORT = os.environ.get("SOLR_PORT", "8983")
SOLR_SERVER = f"{SOLR_HOST}:{SOLR_PORT}"
SOLR_CORE = "books"  # Probably the best way to do this is to keep this always books, and solr will be initialized with a single core called books with a schema specified in an env var


def make_query_raw(query):
    return requests.get(f"http://{SOLR_SERVER}/solr/{SOLR_CORE}/query?{query}").json()


def make_query_basic(q="", fl="*, [child]", rows=10, start=0, sort="score desc", exact=False):
    # TODO this function probably should be improved to handle more complex queries
    #      and we could even create more highlevel wrappers as needed

    result = str((TextBlob(q)).correct())

    final_q = 'content_type: "BOOK"' + \
        (" AND " + f'text:"{result}"' if result else "")

    return {
        "exact_query": exact,
        "orig_query": q,
        "did_you_mean": result,
        "docs": make_query_raw(f"q={final_q}&fl={fl}&rows={rows}&start={start}&sort={sort}")['response']['docs']
    }


def make_query_quote(q="", fl="*, [child]", rows=10, start=0, sort="score desc", exact=False):

    result = str((TextBlob(q)).correct())

    final_q = 'content_type: "BOOK"' + \
        (" AND " + f'text:"{result}"' if result else "")

    return {
        "exact_query": exact,
        "orig_query": q,
        "did_you_mean": result,
        "docs": make_query_raw(f"q={final_q}&fl={fl}&rows={rows}&start={start}&sort={sort}")['response']['docs']
    }
