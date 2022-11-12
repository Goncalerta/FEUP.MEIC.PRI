from evaluation import EvaluateQuery
import requests
import sys

QRELS_FILE = "./q1/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?q=title:the",
    "sys2": "http://localhost:8983/solr/books2/select?q=title:the AND author:tolkien",
    "sys3": "http://localhost:8983/solr/books3/select?q=title:the AND author:tolkien AND subject:war"
}

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results = requests.get(query[sys.argv[1]]).json()['response']['docs']

qe = EvaluateQuery(results, relevant)

qe.export_metrics(f'q1/{sys.argv[1]}')
qe.plot_precision_recall(f'q1/{sys.argv[1]}')
