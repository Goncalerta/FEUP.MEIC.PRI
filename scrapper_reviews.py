from lib2to3.pgen2.token import NUMBER
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from whoswho import who


def handle_book_title(book_title):
    book_title = book_title.replace(" ", "+")
    book_title = book_title.replace("\r", " ")
    book_title = book_title.replace("\t", " ")
    book_title = book_title.replace("\n", " ")
    return book_title


def fetch_review(book_title, author_name):
    book_title = handle_book_title(book_title)
    r = requests.get(
        f"https://www.goodreads.com/search?q={book_title.replace(' ', '+')}")
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', class_='tableList')

    if (not table):
        r = requests.get(
            f"https://www.goodreads.com/search?q={book_title.split(':')[0].replace(' ', '+')}")
        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.find('table', class_='tableList')

        if (not table):
            return None

    rows = table.find_all('tr')
    targetColumns = [row.find_all('td')[1] for row in rows]
    authors = [column.find(
        'a', class_='authorName').find('span').text for column in targetColumns]

    hyperlinks = [targetColumn.find('a', class_='bookTitle')[
        'href'] for idx, targetColumn in enumerate(targetColumns) if who.match(authors[idx], author_name) or author_name == authors[idx]]

    if (hyperlinks != []):
        return hyperlinks[0]

    return None


def save_book(folder, book_info, text):
    book_id = book_info['id']
    book_info['text'] = text
    with open(f"output/{folder}/{book_id}.json", 'w') as f:
        json.dump(book_info, f, indent=4)


def debug_pipeline():
    ORIG_FOLDER = 'debug'
    NEW_FOLDER = 'debug_reviews'

    new_directory = f"output/{NEW_FOLDER}"
    os.makedirs(new_directory, exist_ok=True)
    for file in os.listdir(new_directory):
        os.remove(f"{new_directory}/{file}")

    books = []
    directory = f"output/{ORIG_FOLDER}"
    for file in os.listdir(directory):
        f = open(f"{directory}/{file}")
        books.append(json.load(f))

    for idx, book in enumerate(books):
        print("===============================")
        print(f"Book {idx + 1}: {book['title']}")
        print("-------------------------------")

        first_author = (book['authors'][0]['first_name'] or '') + \
            ' ' + (book['authors'][0]['last_name'] or '')

        print(
            f"Fetching review from Goodreads: {fetch_review(book['title'], first_author.strip() or '')}")
        # save_review(FOLDER, book_info, text)"""


debug_pipeline()
