# Parses the book info into a clean json with the relevant fields
import json
import sys

def parse_book_info(data):
    book_id = data['book_id']

    if 'Subject' not in data:
        data['Subject'] = []

    if 'Author' not in data:
        if 'Translator' in data:  
            print(
                f"🚨 No author found for book {book_id}. Implicitely replacing with 'Translator' {data['Translator']}...")
            data['Author'] = data['Translator']
        else:
            data['Author'] = []

    def aux_parse_author(author):
        author_id = None
        if author['href'] is None:
            print(f"❌ No author ID for book {book_id}", file=sys.stderr)
        else:
            author_href_parts = author['href'].split('/')
            if len(author_href_parts) == 0:
                print(f"❌ Invalid author ID for book {book_id}: {author_href_parts}", file=sys.stderr)
            else:
                author_id = author_href_parts[-1]

        author_text_parts = author['text'].split(',')
        author_last_name = author_text_parts[0].strip()

        author_living_years = [None, None]
        if len(author_text_parts) > 1:
            if '-' in author_text_parts[-1]:
                author_living_years = [x.strip() for x in author_text_parts[-1].split('-')]
                if len(author_living_years) != 2:
                    print(f"❌ Invalid author living years structure for book {book_id}: {author_living_years}", file=sys.stderr)
                else:
                    author_text_parts = author_text_parts[:-1]
            elif 'century' in author_text_parts[-1]:
                century = author_text_parts[-1].strip()
                author_living_years = [century, century]
                author_text_parts = author_text_parts[:-1]

        author_first_name = None
        author_title = None
        if len(author_text_parts) > 1:
            author_first_name = author_text_parts[1].strip()
        if len(author_text_parts) > 2:
            author_title = ", ".join(author_text_parts[2:]).strip()        

        return {
            'id': author_id,  # last part of the URL
            'last_name': author_last_name,
            'first_name': author_first_name,
            'author_title': author_title,
            'year_of_birth': author_living_years[0],
            'year_of_death': author_living_years[1],
        }

    return {
        'id': book_id,
        'title': data['Title'][0]['text'],
        'authors': [aux_parse_author(author) for author in data['Author']],
        'release_date': data['Release Date'][0]['text'],
        'subjects': [(subject['href'].split('/')[-1], subject['text']) for subject in data['Subject']],
    }

for book in sys.stdin:
    book = json.loads(book.strip())
    data = parse_book_info(book)
    print(json.dumps(data))
