import json
import os
import sys
import re
import unicodedata


def count_author_books():
    author_id_to_name = {}
    author_book_counts = {}
    for idx, file in enumerate(os.listdir("output/books")):
        print(f"{idx}/8000 Processing file: {file}", file=sys.stderr)
        with open("output/books/" + file, "r") as f:
            author_lst = json.load(f)['authors']

            for author in author_lst:
                if (author['id'] not in author_id_to_name):
                    author_id_to_name[author['id']
                                      ] = f"{author['first_name'] or ''} {author['last_name'] or ''}".strip().encode('ascii', 'ignore').decode('ascii')
                author_book_counts[author_id_to_name[author['id']]] = author_book_counts.get(
                    author_id_to_name[author['id']], 0) + 1

    print(f"ALL DONE; NOW SAVING", file=sys.stderr)
    for k, v in author_book_counts.items():
        print(f"{k},{v}")

    print("OVER", file=sys.stderr)


count_author_books()
