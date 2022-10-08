import json
import os
import requests
from bs4 import BeautifulSoup
import re
from whoswho import who

# HACK For some reason emojis in debug messages don't work if I don't do this
#      the problem happens with commands such as "python scrapper_books.py > debug.txt"
import sys


def print(s, end='\n'):
    sys.stdout.buffer.write(f"{s}{end}".encode('utf8'))
    sys.stdout.buffer.flush()


def remove_simple_paragraphs(txt):
    return (txt
            .replace("\r\n\r\n", "?!THISISESCAPE_BALTA_PG_MIRO!?")
            .replace("\r\n", " ")
            .replace("?!THISISESCAPE_BALTA_PG_MIRO!?", "\r\n")
            )


def retrieve_book_id(book_review_link):
    print(book_review_link)
    match = re.search('/book/show/(\d+)', book_review_link)
    if match:
        return match.group(1)
    return None


def handle_book_title(book_title):
    book_title = book_title.replace("\r", " ")
    book_title = book_title.replace("\t", " ")
    book_title = book_title.replace("\n", " ")
    return book_title


def author_match(author_name, authors):
    if (not author_name):
        return True
    for author in authors:
        if who.match(author_name, author) or author_name == author:
            return True
    return False


def fetch_review(book_title, author_name):
    book_title = handle_book_title(book_title)
    r = requests.get(
        f"https://www.goodreads.com/search?q={book_title.replace(' ', '+')}")
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table', class_='tableList')

    # Some book titles might have a unnoficial subtitle, depending on the book version
    # Even with different subtitles, the books might be the same
    # Since the query for such book might fail due to the subtitle, we try to remove it

    if (not table):
        new_book_title = book_title.split(':')[0]
        print(
            f"❌ No review found for '{book_title}'. 🔃 Trying '{new_book_title}' 🔃")
        r = requests.get(
            f"https://www.goodreads.com/search?q={new_book_title.replace(' ', '+')}")
        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.find('table', class_='tableList')

        if (not table):
            print(
                f"❌ No review found for {new_book_title}.")
            return None

    rows = table.find_all('tr')
    targetColumns = [row.find_all('td')[1] for row in rows]
    authors = [[authorLink.find('span').text for authorLink in column.find_all(
        'a', class_='authorName')] for column in targetColumns]

    hyperlinks = [targetColumn.find('a', class_='bookTitle')[
        'href'] for idx, targetColumn in enumerate(targetColumns) if author_match(author_name, authors[idx])]

    if (hyperlinks != []):
        return hyperlinks[0]

    return None


def get_rating(book, num_tries=10):

    first_author = None
    if (book['authors']):
        first_author = ((book['authors'][0]['first_name'] or '') +
                        ' ' + (book['authors'][0]['last_name'] or '')).strip()
    else:
        print("🚨 No author in book, fetched reviews might not be accurate")

    book_review_link = fetch_review(
        book['title'], first_author)

    if (not book_review_link):
        print("❌ No book review found ")
        return (None, None)

    book_id = retrieve_book_id(book_review_link)

    if (not book_id):
        print("❌ No book ID found")
        return (None, None)

    for _ in range(num_tries):
        r = requests.get(
            f"https://www.goodreads.com/book/show/{book_id}")
        soup = BeautifulSoup(r.text, 'html.parser')

        ratings = soup.find(
            'div', class_='BookPageMetadataSection__ratingStats')

        if not ratings:
            continue

        average_rating = ratings.find(
            'div', class_='RatingStatistics__rating').text
        review_stats = ratings.find('div', class_='RatingStatistics__meta')[
            'aria-label']
        return (average_rating, review_stats)

    return (None, None)


def parse_review_stats(review_stats):
    if (review_stats == None):
        return (None, None)

    review_stats = review_stats.replace(',', '')
    match = re.search('(\d+) ratings and (\d+) reviews', review_stats)
    if match:
        return (match.group(1), match.group(2))

    return (None, None)


for idx, file in enumerate(os.listdir("output/books")):
    print(f"{idx + 1}/8000 Processing file: {file}")
    with open("output/books/" + file, "r+") as f:
        data = json.load(f)
        data['text'] = remove_simple_paragraphs(data['text'])
        average_rating, review_stats = get_rating(data)
        num_ratings, num_reviews = parse_review_stats(review_stats)
        data['average_rating'] = average_rating
        data['num_ratings'] = num_ratings
        data['num_reviews'] = num_reviews
        f.seek(0)
        json.dump(data, f)
        f.truncate()
