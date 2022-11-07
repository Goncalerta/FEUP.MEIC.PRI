import os
import json
import re
import math
import matplotlib.pyplot as plt
import numpy as np
import unicodedata

from year_of_birth_count import GEN_GRAPH

WARNINGS = False
GEN_GRAPH = True
SOURCE_DIR = "output/books/"
DEST_DIR = "output/stats/"
DEST_FILE = "rat_book_count.json"


def warn(message):
    if WARNINGS:
        print(message)


def split_words(txt):
    encoded_str = unicodedata.normalize('NFD', txt).encode(
        'ascii', 'ignore').decode('ascii')
    encoded_str = re.sub(r"[^a-zA-Z'\s]", ' ', encoded_str).lower()
    return encoded_str.split()


def get_count():

    book_size_rating = {}
    for idx, entry in enumerate(os.listdir(SOURCE_DIR)):
        print(f"Current book ({idx + 1}/8000): {entry}")
        with open(SOURCE_DIR + entry, 'r') as file:
            info = json.load(file)
            if not info['average_rating']:
                continue

            text_num_words = len(split_words(info['text']))
            book_size_rating[info['id']] = (
                text_num_words, info['average_rating'])

    return book_size_rating


def save_count(count):
    os.makedirs(DEST_DIR, exist_ok=True)
    with open(DEST_DIR + DEST_FILE, 'w') as file:
        json.dump(count, file, indent=4)


def plot_count(count):
    pairs = sorted(count.values(), key=lambda tup: tup[0])

    x_data = [pair[0] for pair in pairs]
    y_data = [float(pair[1]) for pair in pairs]

    plt.scatter(x_data, y_data, c="blue")
    plt.xlim(0, 200000)
    plt.ylim(0, 5)
    plt.locator_params(axis="y", nbins=5)
    plt.xlabel('Number of words')
    plt.ylabel('Rating')
    plt.show()


def main():
    result = get_count()
    save_count(result)
    if GEN_GRAPH:
        plot_count(result)


if __name__ == "__main__":
    main()
