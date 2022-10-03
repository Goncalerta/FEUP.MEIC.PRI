from lib2to3.pgen2.token import NUMBER
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from whoswho import who
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import JavascriptException, ElementNotInteractableException, ElementClickInterceptedException, ElementNotVisibleException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select
import re

RATING_STARS_DICT = {'it was amazing': 5,
                     'really liked it': 4,
                     'liked it': 3,
                     'it was ok': 2,
                     'did not like it': 1,
                     '': None}


def handle_book_title(book_title):
    book_title = book_title.replace("\r", " ")
    book_title = book_title.replace("\t", " ")
    book_title = book_title.replace("\n", " ")
    return book_title


def author_match(author_name, authors):
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
            f"WARNING: No review found for '{book_title}'. Trying '{new_book_title}'")
        r = requests.get(
            f"https://www.goodreads.com/search?q={new_book_title.replace(' ', '+')}")
        soup = BeautifulSoup(r.text, 'html.parser')

        table = soup.find('table', class_='tableList')

        if (not table):
            print(
                f"WARNING: No review found for {new_book_title}.")
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


def switch_reviews_mode(driver, book_id, sort_order, rating=None):
    """
    Copyright (C) 2019 by Omar Einea: https://github.com/OmarEinea/GoodReadsScraper
    Licensed under GPL v3.0: https://github.com/OmarEinea/GoodReadsScraper/blob/master/LICENSE.md
    Accessed on 2019-12-01.
    """
    edition_reviews = False
    rating = str(rating) if rating else ''
    driver.execute_script(
        'document.getElementById("reviews").insertAdjacentHTML("beforeend", \'<a data-remote="true" rel="nofollow"'
        f'class="actionLinkLite loadingLink" data-keep-on-success="true" id="switch{rating}{sort_order}"' +
        f'href="/book/reviews/{book_id}?rating={rating}&sort={sort_order}' +
        ('&edition_reviews=true' if edition_reviews else '') + '">Switch Mode</a>\');' +
        f'document.getElementById("switch{rating}{sort_order}").click()'
    )
    return True


def get_rating(node):
    if len(node.find_all('span', {'class': 'staticStars'})) > 0:
        rating = node.find_all('span', {'class': 'staticStars'})[0]['title']
        return RATING_STARS_DICT[rating]
    return ''


def get_user_name(node):
    if len(node.find_all('a', {'class': 'user'})) > 0:
        return node.find_all('a', {'class': 'user'})[0]['title']
    return ''


def get_user_url(node):
    if len(node.find_all('a', {'class': 'user'})) > 0:
        return node.find_all('a', {'class': 'user'})[0]['href']
    return ''


def get_date(node):
    if len(node.find_all('a', {'class': 'reviewDate createdAt right'})) > 0:
        return node.find_all('a', {'class': 'reviewDate createdAt right'})[0].text
    return ''


def get_text(node):

    display_text = ''
    full_text = ''

    if len(node.find_all('span', {'class': 'readable'})) > 0:
        for child in node.find_all('span', {'class': 'readable'})[0].children:
            if child.name == 'span' and 'style' not in child:
                display_text = child.text
            if child.name == 'span' and 'style' in child and child['style'] == 'display:none':
                full_text = child.text

    if full_text:
        return full_text

    return display_text


def get_num_likes(node):
    if node.find('span', {'class': 'likesCount'}) and len(node.find('span', {'class': 'likesCount'})) > 0:
        likes = node.find('span', {'class': 'likesCount'}).text
        if 'likes' in likes:
            return int(likes.split()[0])
    return 0


def get_shelves(node):
    shelves = []
    if node.find('div', {'class': 'uitext greyText bookshelves'}):
        _shelves_node = node.find(
            'div', {'class': 'uitext greyText bookshelves'})
        for _shelf_node in _shelves_node.find_all('a'):
            shelves.append(_shelf_node.text)
    return shelves


def get_id(bookid):
    pattern = re.compile("([^.]+)")
    return pattern.search(bookid).group()


def fetch_review_info(book_id, num_reviews=10, num_attempts=15):

    community_reviews = None
    """for _ in range(10):
        r = requests.get(
            f"https://www.goodreads.com{review_link}")
        soup = BeautifulSoup(r.text, 'html.parser')
        community_reviews = soup.find('div', id='ReviewsSection')
        if (community_reviews):
            break"""

    driver = webdriver.Firefox(executable_path="C:\\Users\\up201906272\\Desktop\\geckodriver.exe")
    url = 'https://www.goodreads.com/book/show/' + book_id
    driver.get(url)
    reviews = []
    
    if num_attempts == 0: return reviews

    try:
        time.sleep(4)

        switch_reviews_mode(driver, book_id, 'default')
        time.sleep(2)

        # Pull the page source, load into BeautifulSoup, and find all review nodes.
        source = driver.page_source
        soup = BeautifulSoup(source, 'lxml')
        nodes = soup.find_all('div', {'class': 'review'})
        book_title = soup.find(id='bookTitle').text.strip()

        # Iterate through and parse the reviews.
        for node in nodes:
            review_id = re.search('[0-9]+', node['id']).group(0)
            reviews.append({'date': get_date(node),
                            'rating': get_rating(node),
                            'user_name': get_user_name(node),
                            'text': get_text(node),
                            'num_likes': get_num_likes(node)})
            num_reviews = num_reviews - 1
            if (num_reviews <= 0):
                break

    except ElementClickInterceptedException:
        print(f'🚨 ElementClickInterceptedException (Likely a pop-up)🚨\n🔄 Refreshing Goodreads site and rescraping book🔄')
        reviews = fetch_review_info(book_id, num_reviews, num_attempts - 1)

    except ElementNotInteractableException:
        print('🚨 ElementNotInteractableException🚨 \n🔄 Refreshing Goodreads site and rescraping book🔄')
        reviews = fetch_review_info(book_id, num_reviews, num_attempts - 1)

    except JavascriptException:
        print('🚨 JavascriptException \n🔄 Refreshing Goodreads site and rescraping book🔄')
        reviews = fetch_review_info(book_id, num_reviews, num_attempts - 1)

    except:
        print('🚨 UnknownException \n🔄 Refreshing Goodreads site and rescraping book🔄')
        reviews = fetch_review_info(book_id, num_reviews, num_attempts - 1)

    driver.close()
    return reviews

    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    community_reviews = soup.find('div', id='ReviewsSection')
    if (not community_reviews):
        print("WARNING: No community reviews found")
        return None

    review_statistics = community_reviews.find(
        'div', class_='ReviewsSectionStatistics')

    review_average_rating = review_statistics.find(
        'div', class_='RatingStatistics__rating').text
    num_of_reviews = review_statistics.find(
        'div', class_='RatingStatistics__meta')['aria-label']

    print(review_average_rating)
    print(num_of_reviews)
    percentage_reviews_raw = review_statistics.find_all(
        'div', class_="RatingsHistogram__labelTotal")

    percentage_reviews = {}
    for percentage in percentage_reviews_raw:
        percentage_reviews[int(percentage['data-testid']
                               [-1])] = percentage.text

    print(percentage_reviews)

    for review in retrieve_top_reviews(community_reviews.find_all('class', class_="ReviewsList"), num_reviews):
        print(review)
    return None"""


def retrieve_book_id(book_review_link):
    print(book_review_link)
    match = re.search('/book/show/(\d+)', book_review_link)
    if match:
        return match.group(1)
    return None


def save_review(folder, book_info, book_id):
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

        book_review_link = fetch_review(
            book['title'], first_author.strip() or '')
        book_id = retrieve_book_id(book_review_link)

        if (not book_id):
            print("WARNING: No book ID found")
            continue

        book_review_info = fetch_review_info(book_id)

        save_review(NEW_FOLDER, book_review_info, book['id'])


debug_pipeline()
