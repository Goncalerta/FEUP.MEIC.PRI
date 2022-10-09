# Detects if two instances with different ids refer to the same book, only printing the first one
import sys
import json
known = set()

def watch_for_duplicates(data):
    book_id = book['book_id']
    if book_id in known:
        print(f"Duplicate book_id: {book_id}", file=sys.stderr)
        return
    known.add(book_id)
    for note in data['Note']:
        if "lso available" in note['text']:
            print(f"NOTE for {book_id}: {note}", file=sys.stderr)
            known.add(note['href'].split('/')[-1])

    print(json.dumps(data))

for book in sys.stdin:
    book = json.loads(book.strip())
    watch_for_duplicates(book)
