from evaluation import EvaluateQuery
import requests
import os
import matplotlib.pyplot as plt

QRELS_FILE = "./q2/qrels.txt"

query = {
    "sys1": "http://localhost:8983/solr/books/select?defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alove%20text%3Alove)",
    "sys2": "http://localhost:8983/solr/books/select?bq=release_date%3A%5BNOW%2FDAY-6YEAR%20TO%20NOW%2FDAY-2YEAR%5D&defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alov*%5E2%20text%3Alov*)",
    "sys1_syn": "http://localhost:8983/solr/books_syn/select?defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alove%20text%3Alove)",
    "sys2_syn": "http://localhost:8983/solr/books_syn/select?bq=release_date%3A%5BNOW%2FDAY-6YEAR%20TO%20NOW%2FDAY-2YEAR%5D&defType=edismax&fl=id%2C%20title%2C%20release_date%2C%20subjects%2C%20content_type%2C%20text%2C%20last_name%2C%20first_name%2C%20authors%2C%20%5Bchild%20fl%3D%22first_name%2Clast_name%22%5D&hl.fl=text&hl=true&indent=true&q.op=AND&q=subjects%3Afiction%20(subjects%3Alov*%5E2%20text%3Alov*)",
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

plt.legend(["sys1", "sys2", "sys1_syn", "sys2_syn"])

plt.savefig('q2/precision_recall.pdf')

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
