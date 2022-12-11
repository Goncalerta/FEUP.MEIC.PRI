import requests
import os

SOLR_HOST = os.environ.get("SOLR_HOST", "solr")
SOLR_PORT = os.environ.get("SOLR_PORT", "8983")
SOLR_SERVER = f"{SOLR_HOST}:{SOLR_PORT}"
SOLR_CORE = "books"  # Probably the best way to do this is to keep this always books, and solr will be initialized with a single core called books with a schema specified in an env var


def make_query_raw(query):
    return requests.get(f"http://{SOLR_SERVER}/solr/{SOLR_CORE}/query?{query}").json()


def make_query(q="*", fl="*", rows=10, start=0, sort="score desc"):
    # TODO this function probably should be improved to handle more complex queries
    #      and we could even create more highlevel wrappers as needed
    return make_query_raw(f"q={q}&fl={fl}&rows={rows}&start={start}&sort={sort}")['response']['docs']

def get_categories():
    facets = make_query_raw("q=content_type:BOOK&q.op=OR&indent=true&facet=true&facet.field=subjects_facet&facet.limit=-1&rows=0")["facet_counts"]["facet_fields"]["subjects_facet"]
    return [facets[i] for i in range(0, len(facets), 2)]
