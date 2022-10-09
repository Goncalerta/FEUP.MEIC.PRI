# Fetches book transcriptions from gutenberg.org
import requests
import json
import re
import sys

def fetch_book_txt(book_id):
    r = requests.get(f"https://www.gutenberg.org/files/{book_id}/{book_id}-8.txt")
    if r.status_code != 200:
        r = requests.get(f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt")
        if r.status_code != 200:
            r = requests.get(f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt")
            if r.status_code != 200:
                print(f"❌ Book {book_id} has no UTF-8 or ASCII txt encoded file.", file=sys.stderr)
    else:
        print(f"👍 Book {book_id} has UTF-8 txt encoded file.", file=sys.stderr)
    
    return r.text

def save_book(folder, book_info, text):
    book_id = book_info['id']
    book_info['text'] = text
    with open(f"{folder}/{book_id}.json", 'w') as f:
        json.dump(book_info, f)
                
for idx, book in enumerate(sys.stdin):
    book = json.loads(book.strip())
    print(f"{idx + 1} Fetching transcription for: {book['id']}", file=sys.stderr)
    text = fetch_book_txt(book['id'])
    save_book(sys.argv[1], book, text)
