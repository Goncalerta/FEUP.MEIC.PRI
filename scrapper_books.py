from lib2to3.pgen2.token import NUMBER
import requests
from bs4 import BeautifulSoup
import json
import os
import re


def fetch_books(page=0):
    r = requests.get(
        f"https://www.gutenberg.org/ebooks/search/?sort_order=downloads&start_index={page*25+1}")
    soup = BeautifulSoup(r.text, 'html.parser')

    links = [a['href'] for a in soup.find_all('a', href=True)]
    links = [link for link in links if link.startswith(
        '/ebooks/') and len(link) > 8 and link[8].isdigit()]
    book_ids = [link.split('/')[-1] for link in links]

    return book_ids


def fetch_books_generator(num_books):
    page = 0
    if num_books <= 0:
        return
    while True:
        for book in fetch_books(page):
            yield book
            num_books -= 1
            if num_books <= 0:
                return
        page += 1


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

    return data


def fetch_book_txt(book_id):
    # Dunno if this might ever be useful, but they offer zipped txts too
    # it could be useful to avoid our dataset disk usage becoming too large, but im sure we won't be able to use it for what we want
    # https://www.gutenberg.org/files/42671/42671.zip
    # TODO this link looks better updated (not cached, so less errors) but have to be careful with encoding mode https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt
    r = requests.get(
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt")

    # The next part tries to filter out the header and footer of the file that is not the book
    # That is hard because some books contain mistakes in the delimiter, so TODO check if this is working for all books
    text = r.text
    text = re.split(r'\*\*\*\s?START[^*]*\*\*\*\s', text, maxsplit=1)
    if len(text) != 2:
        print(
            f"🚨 Book {book_id} has no start of the project gutenberg ebook")

    text = text[1]
    text = re.split(r'\*\*\*\s?END[^*]*\*\*\*\s', text, maxsplit=1)
    if len(text) != 2:
        print(
            f"🚨 Book {book_id} has no end of the project gutenberg ebook")

    text = text[0]
    text = text.strip()

    # this function is returning a lot of transcribed things (title, author, editor notes, chapter names, etc)
    # I think each book has a different structure regarding that so i can't think of a way to parse the structure of filter those extra things
    # nor if we even want to do that
    return text


def parse_book_info_table(data):
    book_id = data['book_id']

    # HACK to allow books without authors
    if 'Author' not in data:
        if 'Translator' in data:  # TODO should we do this?
            print(
                f"🚨 No author found for book {book_id}. Implicitely replacing with 'Translator' {data['Translator']}...")
            data['Author'] = data['Translator']

    EXPECT_EXACTLY_ONE = ['Title', 'Language',
                          'Release Date', 'Copyright Status', 'EBook-No.']
    for key in EXPECT_EXACTLY_ONE:
        if key not in data or len(data[key]) == 0:
            print(f"🚨 No column '{key}' for book {book_id}")
        if len(data[key]) > 1:
            print(f"🚨 More than one column '{key}' for book {book_id}")

    if 'Subject' not in data:
        data['Subject'] = []
    if 'Note' not in data:
        data['Note'] = []

    for note in data['Note']:
        if "improved" in note['text']:
            print(f"NOTE: for {book_id}: {note}")

    if book_id != data['EBook-No.'][0]['text']:
        print(
            f"🚨 Book ID mismatch for book {book_id}: {data['EBook-No.'][0]['text']}")

    if data['Copyright Status'][0]['text'] != 'Public domain in the USA.':
        print(
            f"🚨 Unexpected copyright status for book {book_id}: {data['Copyright Status'][0]['text']}")

    def aux_parse_author(author):
        if author['href'] is None:
            print(f"🚨 No author ID for book {book_id}")

        author_href_parts = author['href'].split('/')
        author_text_parts = author['text'].split(',')

        if len(author_href_parts) == 0:
            print(
                f"🚨 Invalid author ID for book {book_id}: {author_href_parts}")

        if len(author_text_parts) == 2:
            print(
                f"🚨 Author is missing a first name {book_id}: {author_text_parts}")
            author_text_parts = [author_text_parts[0],
                                 None, author_text_parts[1]]
            author_text_parts[0] = author_text_parts[0].strip()
        elif len(author_text_parts) != 3:
            print(
                f"🚨 Invalid author name structure for book {book_id}: {author_text_parts}")
        else:
            author_text_parts[0] = author_text_parts[0].strip()
            author_text_parts[1] = author_text_parts[1].strip()
            author_text_parts[2] = author_text_parts[2].strip()

        author_living_years = author_text_parts[2].split('-')
        if len(author_living_years) != 2:
            print(
                f"🚨 Invalid author living years structure for book {book_id}: {author_living_years}")

        return {
            'id': author_href_parts[-1],  # last part of the URL
            'last_name': author_text_parts[0],  # before the comma
            'first_name': author_text_parts[1],  # after first comma
            'year_of_birth': author_living_years[0],
            'year_of_death': author_living_years[1],
        }

    # Some things that I am currently discarting but may end up being useful in the future
    # - Equivalent book note: "Note     This title is also available as ...""
    # - Wikipedia link note
    # - Other notes?
    # - LoC class
    # - Category
    # - Illustrator
    # - Original Publication

    # I am not yet filtering by language

    return {
        'id': book_id,
        'title': data['Title'][0]['text'],
        'language': data['Language'][0]['text'],
        'authors': [aux_parse_author(author) for author in data['Author']],
        'release_date': data['Release Date'][0]['text'],
        'subjects': [(subject['href'].split('/')[-1], subject['text']) for subject in data['Subject']],
    }


def save_book(folder, book_info, text):
    book_id = book_info['id']
    book_info['text'] = text
    with open(f"output/{folder}/{book_id}.json", 'w') as f:
        json.dump(book_info, f, indent=4)


def debug_pipeline(num_books):
    FOLDER = 'debug'
    os.makedirs(f"output/{FOLDER}", exist_ok=True)
    for file in os.listdir(f"output/{FOLDER}"):
        os.remove(f"output/{FOLDER}/{file}")

    for idx, book in enumerate(fetch_books_generator(num_books)):
        print("===============================")
        print(f"Book {idx + 1}/{num_books}: /ebooks/{book}")
        print("-------------------------------")
        raw_book_info = fetch_book_info_table(book)
        book_info = parse_book_info_table(raw_book_info)
        text = fetch_book_txt(book)
        save_book(FOLDER, book_info, text)


debug_pipeline(30)
