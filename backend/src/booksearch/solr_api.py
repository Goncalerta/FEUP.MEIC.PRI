import requests
import os
from textblob import TextBlob

SOLR_HOST = os.environ.get("SOLR_HOST", "solr")
SOLR_PORT = os.environ.get("SOLR_PORT", "8983")
SOLR_SERVER = f"{SOLR_HOST}:{SOLR_PORT}"
SOLR_CORE = "books"  # Probably the best way to do this is to keep this always books, and solr will be initialized with a single core called books with a schema specified in an env var


def make_query_raw(query):
    return requests.get(f"http://{SOLR_SERVER}/solr/{SOLR_CORE}/query?{query}").json()


def mlt_query_raw(query):
    return requests.get(f"http://{SOLR_SERVER}/solr/{SOLR_CORE}/mlt?{query}").json()


def make_query_basic(q="", fl="*, [child]", rows=10, start=0, sort="score desc", exact=False):
    fields = ["title", "subjects", "text"]
    final_q = 'content_type: "BOOK"'
    result = ""

    def boost(field):
        if field == "title":
            return 1
        if field == "subjects":
            return 1.5
        if field == "text":
            return 1

    for keyword in q.split():
        keyword_did_you_mean = keyword if exact else str(
            (TextBlob(keyword)).correct())
        result += keyword_did_you_mean + " "
        final_q += " AND (" + (" OR ").join([
            f'({field}:"{keyword_did_you_mean}"~)^{boost(field)}' for field in fields]) + ")"

    return {
        "exact_query": exact,
        "orig_query": q,
        "final_q": final_q,
        "did_you_mean": result.strip(),
        "docs": make_query_raw(f"q={final_q}&fl={fl}&rows={rows}&start={start}&sort={sort}")['response']['docs']
    }


def make_query_exact(finalq, fl="*, [child]", rows=10, start=0, sort="score desc", exact=True):
    return {
        "exact_query": exact,
        "orig_query": finalq,
        "final_q": finalq,
        "did_you_mean": finalq,
        "docs": make_query_raw(f"q={finalq}&fl={fl}&rows={rows}&start={start}&sort={sort}")['response']['docs']
    }


def make_query_advanced(
        q="", fl="*, [child]", rows=10, start=0, sort="score desc", exact=False, title="", releasedAfter="", releasedBefore="",
        category="", ratingMin="", ratingMax="", minNumRating="", maxNumRating="", authorFirstName="", authorLastName="", aliveAfter="", aliveBefore=""):
    fields = ["title", "subjects", "text"]
    final_q = 'content_type: "BOOK"'
    result = ""

    def boost(field):
        if field == "title":
            return 1
        if field == "subjects":
            return 1.5
        if field == "text":
            return 1

    if q is not None:
        for keyword in q.split():
            keyword_did_you_mean = keyword if exact else str(
                (TextBlob(keyword)).correct())
            result += keyword_did_you_mean + " "
            final_q += " AND (" + (" OR ").join([
                f'({field}:"{keyword_did_you_mean}"~)^{boost(field)}' for field in fields]) + ")"
    else:
        q = ""
        result = ""

    if title is not None:
        final_q += f' AND title:"{title}"~'
    if category is not None:
        final_q += f' AND subjects:"{category}"~'
    if ratingMin is not None and ratingMax is not None:
        final_q += f' AND rating:[{ratingMin} TO {ratingMax}]'
    elif ratingMin is not None:
        final_q += f' AND rating:[{ratingMin} TO *]'
    elif ratingMax is not None:
        final_q += f' AND rating:[* TO {ratingMax}]'

    if minNumRating is not None and maxNumRating is not None:
        final_q += f' AND num_ratings:[{minNumRating} TO {maxNumRating}]'
    elif minNumRating is not None:
        final_q += f' AND num_ratings:[{minNumRating} TO *]'
    elif maxNumRating is not None:
        final_q += f' AND num_ratings:[* TO {maxNumRating}]'

    if releasedAfter is not None:
        releasedAfter = releasedAfter[:19] + 'Z'
    if releasedBefore is not None:
        releasedBefore = releasedBefore[:19] + 'Z'

    if releasedAfter is not None and releasedBefore is not None:
        final_q += f' AND release_date:[{releasedAfter} TO {releasedBefore}]'
    elif releasedAfter is not None:
        final_q += f' AND release_date:[{releasedAfter} TO *]'
    elif releasedBefore is not None:
        final_q += f' AND release_date:[* TO {releasedBefore}]'

    if authorFirstName is not None or authorLastName is not None or aliveAfter is not None or aliveBefore is not None:
        final_q = final_q.replace('"', '\\"')
        final_q = '{' + f'!parent which="{final_q}"' + '}'

    sub_q = ''
    if authorFirstName is not None:
        sub_q += f' AND first_name:"{authorFirstName}"~'

    if authorLastName is not None:
        sub_q += f' AND last_name:"{authorLastName}"~'

    if aliveAfter is not None:
        aliveAfter = aliveAfter[:4]
        sub_q += f' AND year_of_death:[{aliveAfter} TO *]'

    if aliveBefore is not None:
        aliveBefore = aliveBefore[:4]
        sub_q += f' AND year_of_birth:[* TO {aliveBefore}]'

    final_q += sub_q[5:]

    return {
        "exact_query": exact,
        "orig_query": q,
        "final_q": final_q,
        "did_you_mean": result.strip(),
        "docs": make_query_raw(f"q={final_q}&fl={fl}&rows={rows}&start={start}&sort={sort}")['response']['docs']
    }


def make_query_quote(q="", fl="*, [child]", rows=10, start=0, sort="score desc", exact=False):

    result = str((TextBlob(q)).correct())
    if exact:
        final_q = 'content_type: "BOOK"' + \
            (" AND " + f'text:"{q}"~' if result else "")
    else:
        final_q = 'content_type: "BOOK"' + \
            (" AND " + f'text:"{result}"~' if result else "")
    print(final_q)

    query = make_query_raw(
        f"hl.fl=text&hl=true&indent=true&hl.simple.pre=<strong>&hl.simple.post=</strong>&q={final_q}")

    docs = query['response']['docs']
    print(query['highlighting'])
    # add highlight field to each doc
    for i in range(len(docs)):
        if query['highlighting'][docs[i]['id']] and len(query['highlighting'][docs[i]['id']]['text']) > 0:
            docs[i]['highlight'] = query['highlighting'][docs[i]['id']]['text'][0]

    return {
        "exact_query": exact,
        "orig_query": q,
        "did_you_mean": result,
        "final_q": final_q,
        "quote": True,
        "docs": docs,
    }


def get_categories():
    facets = make_query_raw("q=content_type:BOOK&q.op=OR&indent=true&facet=true&facet.field=subjects_facet&facet.limit=-1&rows=0")[
        "facet_counts"]["facet_fields"]["subjects_facet"]
    return [facets[i] for i in range(0, len(facets), 2)]


def more_like_this(q=0, fl="*, [child]", rows=10, start=0, sort="score desc"):
    mlt = mlt_query_raw(f"q=id:{q}&fl={fl}&rows={rows}&start={start}&sort={sort}")[
        "response"]
    mlt['docs'] = [doc for doc in mlt['docs'] if doc['content_type'] == "BOOK"]
    mlt['num_found'] = len(mlt['docs'])
    return mlt


def get_book(id):
    return make_query_raw(f"q=id:{id}%20content_type:BOOK&q.op=AND&indent=true&rows=1&fl=*,%5Bchild%5D")['response']['docs'][0]
