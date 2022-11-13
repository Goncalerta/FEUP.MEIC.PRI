from evaluation import EvaluateQuery
import requests
import os
import matplotlib.pyplot as plt

QRELS_FILE = "./q4/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?indent=true&q.op=OR&q=text%3A%22want%20nto%2C%20waste%20not%22",
    "sys2": "http://localhost:8983/solr/books/select?hl.fl=text&hl=true&indent=true&q.op=OR&q=text%3A%22want%20nto%2C%20waste%20not%22~5",
    "sys1_syn": "http://localhost:8983/solr/books_syn/select?indent=true&q.op=OR&q=text%3A%22want%20nto%2C%20waste%20not%22",
    "sys2_syn": "http://localhost:8983/solr/books_syn/select?hl.fl=text&hl=true&indent=true&q.op=OR&q=text%3A%22want%20nto%2C%20waste%20not%22~5",
}

relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))

results_dict = {}

plt.ylim(0, 1)


for system, url in query.items():
    # Read qrels to extract relevant documents
    # Get query results from Solr instance
    results = requests.get(url).json()['response']['docs']

    results = [x['id'] for x in results]

    results_dict[system] = results

    qe = EvaluateQuery(results, relevant)
    path = f'q4/{system}'
    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(path):

        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(path)

    qe.export_metrics(path)
    qe.plot_precision_recall(path)
    qe.export_ap(path)

plt.legend(["sys1", "sys2", "sys1_syn", "sys2_syn"])

plt.savefig('q1/precision_recall.pdf')

for i in range(10):
    sys1_r = ('R' if results_dict['sys1'][i]
              in relevant else 'I') if results_dict['sys1'] and i < len(results_dict['sys1']) else 'N/A'
    sys1_syn_r = ('R' if results_dict['sys1_syn'][i]
                  in relevant else 'I') if results_dict['sys1_syn'] and i < len(results_dict['sys1_syn']) else 'N/A'
    sys2_r = ('R' if results_dict['sys2'][i]
              in relevant else 'I') if results_dict['sys2'] and i < len(results_dict['sys2']) else 'N/A'
    sys2_syn_r = ('R' if results_dict['sys2_syn'][i]
                  in relevant else 'I') if results_dict['sys2_syn'] and i < len(results_dict['sys2_syn']) else 'N/A'
    print(
        f"{i+1} & {sys1_r} & {sys2_r} & {sys1_syn_r} & {sys2_syn_r} \\\\")
