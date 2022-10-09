# For each book_id in stdin, fetches it's book table and converts it into a json printing it to the stdout. 
# If an improved version of the book is detected during the fetch, the improved version is fetched instead. 

import requests
import sys
import json
from bs4 import BeautifulSoup

def fetch_book_info_table(book_id):
    r = requests.get(f"https://www.gutenberg.org/ebooks/{book_id}")
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', class_='bibrec')
    rows = table.find_all('tr')
    rows = [row.find_all('th') + row.find_all('td') for row in rows]
    rows = [row for row in rows if len(row) > 1]

    data = {}

    def aux_parse_column(column):
        return {
            'text': column.text.strip(),
            'href': column.find('a')['href'] if column.find('a') else None
        }

    for row in rows:
        key = row[0].text
        data[key] = data.get(key, []) + [aux_parse_column(column)
                                         for column in row[1:]]

    data['book_id'] = book_id

    if 'Note' not in data:
        data['Note'] = []

    for note in data['Note']:
        if "improved" in note['text']:
            print(f"NOTE for {book_id}: {note}", file=sys.stderr)
            return fetch_book_info_table(note['href'].split('/')[-1])

    print(json.dumps(data))

for book_id in sys.stdin:
    book_id = book_id.strip()
    fetch_book_info_table(book_id)
    
