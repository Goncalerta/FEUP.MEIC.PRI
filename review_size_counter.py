import json
import os
import sys
import re
import unicodedata
import matplotlib.pyplot as plt


def split_words(txt):
    encoded_str = unicodedata.normalize('NFD', txt).encode(
        'ascii', 'ignore').decode('ascii')
    encoded_str = re.sub(r"[^a-zA-Z'\s]", ' ', encoded_str).lower()
    return encoded_str.split()


def count_review_size_rating():
    vals = {}
    for idx, file in enumerate(os.listdir("output/reviews")):
        print(f"{idx + 1}/830 Processing file: {file}", file=sys.stderr)
        with open("output/reviews/" + file, "r") as f:
            file = json.load(f)
            for review in file:
                if not review['rating']:
                    continue
                num_words = len(split_words(review['text']))
                rating = int(review['rating'])

                vals[rating] = vals.get(rating, []) + [num_words]

    for k, v in vals.items():
        vals[k] = sum(v) / len(v)

    plt.bar(list(vals.keys()), list(vals.values()), color="blue")

    plt.xlabel('Review Rating')
    plt.ylabel('Mean number of words in review')
    plt.show()


count_review_size_rating()
