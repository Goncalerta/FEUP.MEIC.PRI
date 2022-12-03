import os
import json

books = os.listdir("solr/merge")
expressions = []

with open("expressions.txt") as f:
    for line in f:
        expressions.append(line.strip().split("\t")[0].strip().lower())

expressions_book_count = {}
expression_count = {k: 0 for k in expressions}
expression_books = {k: [] for k in expressions}

for book in books:
    with open(f"solr/merge/{book}", encoding='utf8') as f:
        databook = json.load(f)
        print(f'Processing book {databook["id"]}')
        expressions_book_count[databook["id"]] = {}

        for expression in expressions:
            count = databook['text'].lower(
            ).count(expression)
            if count > 0:
                print(f'Found {expression} in {databook["id"]}')
                expressions_book_count[databook["id"]][expression] = count
                expression_count[expression] += 1
                expression_books[expression].append(databook["id"])

items = [(k, v) for k, v in expression_count.items()]

sorted_items = sorted(items, key=lambda x: x[1], reverse=True)

json_sorted_items = [{"expression": k, "count": v, "books": {i: expressions_book_count[i][k] for i in expression_books[k]}}
                     for k, v in sorted_items]

json.dump(json_sorted_items, open(
    "book_quotes.json", "w+"), ensure_ascii=True)
