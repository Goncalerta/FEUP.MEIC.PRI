# Filters out entries that have no value or multiple values for the given columns 
import json
import sys

def expect_exact_1(data):
    book_id = data['book_id']
    
    for key in sys.argv[1:]:
        if key not in data or len(data[key]) == 0:
            print(f"❌ No column '{key}' for book {book_id}", file=sys.stderr)
            return
        if len(data[key]) > 1:
            print(f"❌ More than one column '{key}' for book {book_id}", file=sys.stderr)
            return 
    
    print(json.dumps(data))
    
for book in sys.stdin:
    book = json.loads(book.strip())
    expect_exact_1(book)
