import os
import json

cats_books = {}
cats_names = {}

books = os.listdir("solr/merge")

for book in books:
    with open(f"solr/merge/{book}", encoding='utf8') as f:
        databook = json.load(f)
        print(f'Processing book {databook["id"]}')
        for subject in databook["subjects"]:
            if subject['id'] not in cats_names:
                cats_names[subject['id']] = subject['name']
                cats_books[subject['id']] = [databook['id']]
            else:
                cats_books[subject['id']].append(databook['id'])

items = [(k, v) for k, v in cats_books.items()]

sorted_items = sorted(items, key=lambda x: len(x[1]), reverse=True)

json_sorted_items = [{"id": k, "name": cats_names[k], "num_books": len(v), "books": v}
                     for k, v in sorted_items]

json.dump(json_sorted_items, open(
    "book_categories.json", "w+"), ensure_ascii=True)
