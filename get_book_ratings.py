import os
import json
import re
import math
import matplotlib.pyplot as plt
import numpy as np
import unicodedata
import sys
from year_of_birth_count import GEN_GRAPH

WARNINGS = False
GEN_GRAPH = True
SOURCE_DIR = "output/books/"
DEST_DIR = "output/stats/"
DEST_FILE = "rat_book_count.json"


def get_count():

    book_rating = []
    for idx, entry in enumerate(os.listdir(SOURCE_DIR)):
        print(f"Current book ({idx + 1}/8000): {entry}", file=sys.stderr)
        with open(SOURCE_DIR + entry, 'r') as file:
            info = json.load(file)
            if not info['average_rating'] or float(info['average_rating']) == 0.0:
                continue

            book_rating.append(info['average_rating'])

    for k, v in enumerate(book_rating):
        print(f"{k},{v}")


get_count()
