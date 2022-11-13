from evaluation import EvaluateQuery
import requests
import os

QRELS_FILE = "./q1/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?df=text&hl.fl=*&hl=true&indent=true&q.op=AND&q=(subjects%3A%20%22economics%22%20OR%20text%3A%22economics%22%20OR%20title%3A%22economics%22)%20(subjects%3A%20%22home%22%20OR%20text%3A%22home%22%20OR%20title%3A%22home%22)",
    "sys2": "http://localhost:8983/solr/books/select?hl.fl=*&hl=true&indent=true&q.op=AND&q=((subjects%3A%20econ*)%5E1.5%20OR%20text%3Aecon*%20OR%20title%3Aecon*)%5E2%20((subjects%3A%20%22home%22~)%5E1.5%20OR%20text%3A%22home%22~%20OR%20title%3A%22home%22~%20)",
    "sys1_syn": "http://localhost:8983/solr/books_syn/select?df=text&hl.fl=*&hl=true&indent=true&q.op=AND&q=(subjects%3A%20%22economics%22%20OR%20text%3A%22economics%22%20OR%20title%3A%22economics%22)%20(subjects%3A%20%22home%22%20OR%20text%3A%22home%22%20OR%20title%3A%22home%22)",
    "sys2_syn": "http://localhost:8983/solr/books_syn/select?hl.fl=*&hl=true&indent=true&q.op=AND&q=((subjects%3A%20econ*)%5E1.5%20OR%20text%3Aecon*%20OR%20title%3Aecon*)%5E2%20((subjects%3A%20%22home%22~)%5E1.5%20OR%20text%3A%22home%22~%20OR%20title%3A%22home%22~%20)"
}

for system, url in query.items():
    # Read qrels to extract relevant documents
    relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
    # Get query results from Solr instance
    results = requests.get(url).json()['response']['docs']

    results = [x['id'] for x in results]

    qe = EvaluateQuery(results, relevant)
    path = f'q1/{system}'
    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(path):

        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(path)

    qe.export_metrics(path)
    qe.plot_precision_recall(path)
    qe.export_ap(path)
