# Fetches the gutenberg catalog, printing <arg0> book_ids, one in each line

import sys
import requests
from bs4 import BeautifulSoup

def fetch_books(page=0):
    r = requests.get(
        f"https://www.gutenberg.org/ebooks/search/?sort_order=downloads&start_index={page*25+1}")
    soup = BeautifulSoup(r.text, 'html.parser')

    links = [a['href'] for a in soup.find_all('a', href=True)]
    links = [link for link in links if link.startswith(
        '/ebooks/') and len(link) > 8 and link[8].isdigit()]
    book_ids = [link.split('/')[-1] for link in links]

    return book_ids


def fetch_books_generator():
    page = 0
    while True:
        for book in fetch_books(page):
            yield book
        page += 1

for idx, book in enumerate(fetch_books_generator()):
    if idx >= int(sys.argv[1]):
        break
    print(book)

