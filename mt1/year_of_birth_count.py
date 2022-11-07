import os
import json
import re
import math
import matplotlib.pyplot as plt
import numpy as np

WARNINGS = False

GEN_GRAPH = True
GRAPH_MIN_YEAR = 1500
GRAPH_MAX_YEAR = 2022
GRAPH_INTERVAL_SIZE = 10

SOURCE_DIR = "output/books/"
DEST_DIR = "output/stats/"
DEST_FILE = "yob_count.json"
BC_TAGS = ('BCE', 'B.C.')
UNCERTAINTY_TAGS = ('?', 'active', 'approximately')
CENTURY_MATCH = "(\d+)(st|nd|rd|th)"
APPROX_CENTURY = "50"


def warn(message):
    if WARNINGS:
        print(message)


def simplify_birth_info(birth_info, tag):
    if tag in birth_info:
        return (birth_info.replace(tag, ''), True)
    return (birth_info, False)


def extract_from_century(birth_info):
    match = re.match(CENTURY_MATCH, birth_info)
    if match:
        return match.groups()[0] + APPROX_CENTURY
    return birth_info


def get_count():

    tally = {}

    for entry in os.listdir(SOURCE_DIR):
        with open(SOURCE_DIR + entry, 'r') as file:
            info = json.load(file)
            authors = info['authors']
            if len(authors) == 0:
                warn(f'No author found for book entry {entry}! Ignoring..')
                continue
            if len(authors) != 1:
                warn(
                    f'Multiple authors found for book entry {entry}! Will use first one.')
            author = authors[0]
            birth_info = author['year_of_death']
            if not birth_info:
                warn(
                    f'No birth year was found on book entry {entry}. Ignoring..')
                continue

            is_bc = False
            uncertain = False

            for bc_tag in BC_TAGS:
                birth_info, matched = simplify_birth_info(birth_info, bc_tag)
                is_bc = is_bc or matched

            for uncertainty_tag in UNCERTAINTY_TAGS:
                birth_info, matched = simplify_birth_info(
                    birth_info, uncertainty_tag)
                uncertain = uncertain or matched

            if is_bc or uncertain:
                birth_info = birth_info.strip()

            birth_info = extract_from_century(birth_info)

            if not birth_info.isdigit():
                warn(
                    f"Non-standard birth info found: {birth_info}\nIgnoring..")
                continue

            birth_year = int(birth_info)
            if is_bc:
                birth_year = -birth_year
            tally[birth_year] = tally.get(birth_year, 0) + 1

    return tally


def save_count(count):
    os.makedirs(DEST_DIR, exist_ok=True)
    with open(DEST_DIR + DEST_FILE, 'w') as file:
        json.dump(count, file, indent=4)


def plot_count(count, min_year, max_year, interval_size):
    pairs = sorted(count.items())
    pairs = filter(lambda pair: min_year <= pair[0] <= max_year, pairs)
    entries = []
    for key, val in pairs:
        entries += [key]*val
    year_delta = entries[-1]-entries[0]+1
    plt.hist(entries, bins=math.ceil(year_delta//interval_size))
    plt.xlabel('Year of Death')
    plt.ylabel('Number of Authors')
    plt.show()


def main():
    result = get_count()
    save_count(result)
    if GEN_GRAPH:
        plot_count(result, GRAPH_MIN_YEAR, GRAPH_MAX_YEAR, GRAPH_INTERVAL_SIZE)


if __name__ == "__main__":
    main()
