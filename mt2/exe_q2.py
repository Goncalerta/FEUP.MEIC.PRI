from evaluation import EvaluateQuery
import requests
import os

QRELS_FILE = "./q2/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alove%20text%3Alove)",
    "sys2": "http://localhost:8983/solr/books/select?bq=release_date%3A%5BNOW%2FDAY-6YEAR%20TO%20NOW%2FDAY-2YEAR%5D&defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alov*%5E2%20text%3Alov*)",
    "sys1_syn": "http://localhost:8983/solr/books_syn/select?defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alove%20text%3Alove)",
    "sys2_syn": "http://localhost:8983/solr/books_syn/select?bq=release_date%3A%5BNOW%2FDAY-6YEAR%20TO%20NOW%2FDAY-2YEAR%5D&defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alov*%5E2%20text%3Alov*)",
}

for system, url in query.items():
    # Read qrels to extract relevant documents
    relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
    # Get query results from Solr instance
    results = requests.get(url).json()['response']['docs']

    results = [x['id'] for x in results]

    qe = EvaluateQuery(results, relevant)
    path = f'q2/{system}'
    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(path):

        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(path)

    qe.export_metrics(path)
    qe.plot_precision_recall(path)
    qe.export_ap(path)
