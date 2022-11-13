from evaluation import EvaluateQuery
import requests
import os

QRELS_FILE = "./q3/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?indent=true&q.op=OR&q=text%3A%22want%20not%2C%20waste%20not%22",
    "sys2": "http://localhost:8983/solr/books/select?hl.fl=text&hl=true&indent=true&q.op=OR&q=text%3A%22want%20not%2C%20waste%20not%22~5",
    "sys1_syn": "http://localhost:8983/solr/books_syn/select?indent=true&q.op=OR&q=text%3A%22want%20not%2C%20waste%20not%22",
    "sys2_syn": "http://localhost:8983/solr/books_syn/select?hl.fl=text&hl=true&indent=true&q.op=OR&q=text%3A%22want%20not%2C%20waste%20not%22~5",
}

for system, url in query.items():
    # Read qrels to extract relevant documents
    relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
    # Get query results from Solr instance
    results = requests.get(url).json()['response']['docs']

    results = [x['id'] for x in results]

    qe = EvaluateQuery(results, relevant)
    path = f'q3/{system}'
    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(path):

        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(path)

    qe.export_metrics(path)
    qe.plot_precision_recall(path)
    qe.export_ap(path)
