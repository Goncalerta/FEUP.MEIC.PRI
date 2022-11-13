from evaluation import EvaluateQuery
import requests
import os
import matplotlib.pyplot as plt

QRELS_FILE = "./q1/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?df=text&hl.fl=*&hl=true&indent=true&q.op=AND&q=(subjects%3A%20%22economics%22%20OR%20text%3A%22economics%22%20OR%20title%3A%22economics%22)%20(subjects%3A%20%22home%22%20OR%20text%3A%22home%22%20OR%20title%3A%22home%22)",
    "sys2": "http://localhost:8983/solr/books/select?hl.fl=*&hl=true&indent=true&q.op=AND&q=((subjects%3A%20econ*)%5E1.5%20OR%20text%3Aecon*%20OR%20title%3Aecon*)%5E2%20((subjects%3A%20%22home%22~)%5E1.5%20OR%20text%3A%22home%22~%20OR%20title%3A%22home%22~%20)",
    "sys1_syn": "http://localhost:8983/solr/books_syn/select?df=text&hl.fl=*&hl=true&indent=true&q.op=AND&q=(subjects%3A%20%22economics%22%20OR%20text%3A%22economics%22%20OR%20title%3A%22economics%22)%20(subjects%3A%20%22home%22%20OR%20text%3A%22home%22%20OR%20title%3A%22home%22)",
    "sys2_syn": "http://localhost:8983/solr/books_syn/select?hl.fl=*&hl=true&indent=true&q.op=AND&q=((subjects%3A%20econ*)%5E1.5%20OR%20text%3Aecon*%20OR%20title%3Aecon*)%5E2%20((subjects%3A%20%22home%22~)%5E1.5%20OR%20text%3A%22home%22~%20OR%20title%3A%22home%22~%20)"
}

relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))

results_dict = {}

# create 

plt.ylim(0, 1)

for system, url in query.items():
    # Read qrels to extract relevant documents
    # Get query results from Solr instance
    results = requests.get(url).json()['response']['docs']

    results = [x['id'] for x in results]

    results_dict[system] = results

    qe = EvaluateQuery(results, relevant)
    path = f'q1/{system}'
    # checking if the directory demo_folder2
    # exist or not.
    if not os.path.isdir(path):

        # if the demo_folder2 directory is
        # not present then create it.
        os.makedirs(path)

    qe.export_metrics(path)
    qe.plot_precision_recall(system)
    qe.export_ap(path)

#qe.plot_precision_recall("q1", ["q1/sys1", "q1/sys2", "q1/sys1_syn", "q1/sys2_syn"])

# plt set legend

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
