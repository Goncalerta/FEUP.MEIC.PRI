import json
import os
import requests
from bs4 import BeautifulSoup
import re
from whoswho import who
import sys





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


def fetch_review(book_title, author_name, attempts=10):
    if (attempts == 0):
        return None

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

    return fetch_review(book_title, None, attempts - 1)


def get_rating(book_id, num_tries=25):
    average_rating = None
    review_stats = None

    for _ in range(num_tries):
        r = requests.get(
            f"https://www.goodreads.com/book/show/{book_id}", timeout=None)
        soup = BeautifulSoup(r.text, 'html.parser')

        ratings = soup.find(
            'div', class_='BookPageMetadataSection__ratingStats')

        if not ratings:
            ratings = soup.find(
                'div', itemprop='aggregateRating')
            if not ratings:
                continue

            average_rating = ratings.find(
                'span', itemprop='ratingValue').text.strip() or average_rating
            rating_count = ratings.find('meta', itemprop='ratingCount')[
                'content'].strip() or None
            review_count = ratings.find('meta', itemprop='reviewCount')[
                'content'].strip() or None

            if not rating_count or not review_count:
                review_stats = None
            else:
                review_stats = f"{rating_count or 0} ratings and {review_count or 0} reviews"
        else:
            average_rating = ratings.find(
                'div', class_='RatingStatistics__rating').text.strip() or average_rating

            review_stats = ratings.find('div', class_='RatingStatistics__meta')[
                'aria-label'].strip() or review_stats

        if not average_rating or not review_stats:
            continue

        return (average_rating, review_stats)

    if not average_rating:
        print("❌ No average rating found")
    if not review_stats:
        print("❌ No review stats found")

    return (average_rating, review_stats)


def parse_review_stats(review_stats):
    if (review_stats == None):
        return (None, None)

    review_stats = review_stats.replace(',', '')
    match = re.search('(\d+) ratings? and (\d+) reviews?', review_stats)
    if match:
        return (match.group(1), match.group(2))

    return (None, None)

# python s <books_folder>
for idx, book_id in enumerate(sys.stdin):
    gutenberg_id, goodreads_id = book_id.split(',')
    print(f"{idx + 1} Processing ratings for: {gutenberg_id}", file=sys.stderr)
    with open(f"{sys.argv[1]}/{gutenberg_id}.json", "r+") as f:
        data = json.load(f)
        
        average_rating, review_stats = get_rating(goodreads_id)
        print("📖 Average rating: ", average_rating)
        num_ratings, num_reviews = parse_review_stats(review_stats)
        print(f"📖 Review stats ({review_stats}): {num_ratings}, {num_reviews}")
        data['average_rating'] = average_rating
        data['num_ratings'] = num_ratings
        data['num_reviews'] = num_reviews

        f.seek(0)
        json.dump(data, f)
        f.truncate()
