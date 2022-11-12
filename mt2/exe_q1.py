from evaluation import EvaluateQuery
import requests
import sys

QRELS_FILE = "./q1/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?df=text&hl.fl=*&hl=true&indent=true&q.op=AND&q=(subjects.name%3A%20%22economics%22%20OR%20text%3A%22economics%22%20OR%20title%3A%22economics%22)%20(subjects.name%3A%20%22home%22%20OR%20text%3A%22home%22%20OR%20title%3A%22home%22)",
    "sys2": "http://localhost:8983/solr/books/select?hl.fl=*&hl=true&indent=true&q.op=AND&q=(subjects.name%3A%20economics%20OR%20text%3Aecon*%20OR%20title%3Aecon*)%5E2%20(subjects.name%3A%20%22home%22~%20OR%20text%3A%22home%22~%20OR%20title%3A%22home%22~%20)",
    "sys3": "http://localhost:8983/solr/books/select?hl.fl=*&hl=true&indent=true&q.op=AND&q=((subjects.name%3A%20econ*)%5E1.5%20OR%20text%3Aecon*%20OR%20title%3Aecon*)%5E2%20((subjects.name%3A%20%22home%22~)%5E1.5%20OR%20text%3A%22home%22~%20OR%20title%3A%22home%22~%20)"
}

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results = requests.get(query[sys.argv[1]]).json()['response']['docs']

results = [x['id'] for x in results]

qe = EvaluateQuery(results, relevant)

qe.export_metrics(f'q1/{sys.argv[1]}')
qe.plot_precision_recall(f'q1/{sys.argv[1]}')
qe.export_ap(f'q1/{sys.argv[1]}')
