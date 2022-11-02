# Filters out entries where the column value doesn't match with the given value
import json
import sys

def filter_by(data):
    book_id = data['book_id']

    key = sys.argv[1]
    for d in data[key]:
        if d['text'] != sys.argv[2]:
            print(f"❌ Unexpected {key} for book {book_id}: {d['text']}", file=sys.stderr)
            return
    
    print(json.dumps(data))
    
for book in sys.stdin:
    book = json.loads(book.strip())
    filter_by(book)
