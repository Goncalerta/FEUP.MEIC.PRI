import json
import os
import re
from datetime import datetime
import xml.etree.cElementTree as ET

MAX_FILES = 8000

files = os.listdir("output/books")

if MAX_FILES == None:
    num_files = len(files)
else:
    num_files = min(MAX_FILES, len(files))

data = []

maxwarnings = 10
for file in files:
    try:
        with open("output/books/" + file, encoding='utf8') as fbook:
            with open("output/reviews/" + file, encoding='utf8') as freview:
                pass
    except FileNotFoundError as e:
        print(f"REVIEW MISSING: {e}")
        maxwarnings -= 1
        if maxwarnings == 0:
            break


def parse_authors(bookid, authors):
    for author in authors:
        author['id'] = f'{bookid}_AUTHOR_{author["id"]}'

        author['content_type'] = "AUTHOR"

        result_birth = re.search(
            r"((\d+)\D\D?BCE)|(\D*(\d+)\D?)", author['year_of_birth']) if author['year_of_birth'] else None
        result_death = re.search(
            r"((\d+)\D\D?BCE)|(\D*(\d+)\D?)", author['year_of_death']) if author['year_of_death'] else None
        if result_birth != None:
            author['year_of_birth'] = -int(result_birth.group(2)
                                           ) if result_birth.group(2) else result_birth.group(4)
        if result_death != None:
            author['year_of_death'] = -int(result_death.group(2)
                                           ) if result_death.group(2) else result_death.group(4)
    return authors


def fix_date(date):
    if not date:
        return date
    date_obj = datetime.strptime(date, "%b %d, %Y").date()
    return f"{date_obj.year}-{date_obj.month}-{date_obj.day}T00:00:00Z"


def parse_subjects(subjects):
    subjects_obj = []
    for subject in subjects:
        subjects_obj.append(subject[1])
    return subjects_obj


def merge_books_and_reviews(fbook, freview):
    databook = json.load(fbook)
    if freview != None:
        datareview = json.load(freview)
        i = 1
        for review in datareview:
            review['content_type'] = "REVIEW"
            review['id'] = f'{databook["id"]}_REVIEW_{i}'
            i += 1
            review['date'] = fix_date(review['date'])

    authors = parse_authors(databook["id"], databook["authors"])
    release_date = fix_date(databook["release_date"])
    subjects = parse_subjects(databook["subjects"])

    if "average_rating" in databook:
        data.append({
            "id": databook["id"],
            "title": databook["title"],
            "authors": authors,
            "release_date": release_date,
            "subjects": subjects,
            "reviews": datareview if freview != None else [],
            "text": databook["text"],
            "rating": databook["average_rating"],
            "num_ratings": databook["num_ratings"],
            "num_reviews": databook["num_reviews"],
            "content_type": "BOOK",
        })
    else:
        print(f"WARNING: Book {databook['id']} has no rating")
        data.append({
            "id": databook["id"],
            "title": databook["title"],
            "authors": authors,
            "release_date": release_date,
            "subjects": subjects,
            "reviews": datareview if freview != None else [],
            "text": databook["text"],
            "content_type": "BOOK",
        })


for idx, file in enumerate(files):
    if idx >= num_files:
        break
    print(f"{idx+1}/{num_files} Processing file: {file}")
    with open("output/books/" + file, encoding='utf8') as fbook:
        try:
            with open("output/reviews/" + file, encoding='utf8') as freview:
                merge_books_and_reviews(fbook, freview)
        except FileNotFoundError as e:
            merge_books_and_reviews(fbook, None)

def parse_element(doc, key, value):
    if value is None or str(value) == "":
        return
    if isinstance(value, list):
        for item in value:
            parse_element(doc, key, item)
    elif isinstance(value, dict):
        subdoc = ET.SubElement(ET.SubElement(doc, "field", name=key), "doc")
        for k, v in value.items():
            parse_element(subdoc, k, v)
    else:
        ET.SubElement(doc, "field", name=key).text = str(value)

for file in data:
    #with open("solr/merge/" + file["id"] + ".json", "w+", encoding='utf8') as f:
    #    json.dump(file, f, ensure_ascii=False)

    root = ET.Element("add")
    doc = ET.SubElement(root, "doc")

    for key, value in file.items():
        parse_element(doc, key, value)

    tree = ET.ElementTree(root)
    tree.write("solr/merge/" + file["id"] + ".xml", encoding='utf8')
