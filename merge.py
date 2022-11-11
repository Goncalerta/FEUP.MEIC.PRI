import json
import os
import re
from datetime import datetime

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


def parse_authors(authors):
    for author in authors:
        author['author_id'] = author['id']
        del author['id']
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
    return f"{date_obj.year}-{date_obj.month}-{date_obj.day}"


def parse_subjects(subjects):
    subjects_obj = []
    for subject in subjects:
        subjects_obj.append({
            'id': subject[0],
            'name': subject[1]
        })
    return subjects_obj


def merge_books_and_reviews(fbook, freview):
    databook = json.load(fbook)
    if freview != None:
        datareview = json.load(freview)
        for review in datareview:
            review['date'] = fix_date(review['date'])

    authors = parse_authors(databook["authors"])
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


for file in data:
    with open("solr/merge/" + file["id"] + ".json", "w+", encoding='utf8') as f:
        json.dump(file, f, ensure_ascii=False)
