import json
import os
import sys
import re
import unicodedata


def count_categories():
    category_counts = {}
    for idx, file in enumerate(os.listdir("output/books")):
        print(f"{idx}/8000 Processing file: {file}", file=sys.stderr)
        with open("output/books/" + file, "r") as f:
            categories = json.load(f)['subjects']

            for category in categories:
                category_str = (category[1].split(
                    '--')[0].split(',')[0]).lower().encode('ascii', 'ignore').decode('ascii')
                category_counts[category_str] = category_counts.get(
                    category_str, 0) + 1

    print(f"ALL DONE; NOW SAVING", file=sys.stderr)
    print('category,count')
    for k, v in category_counts.items():
        print(f"{k},{v}")

    print("OVER", file=sys.stderr)


count_categories()
