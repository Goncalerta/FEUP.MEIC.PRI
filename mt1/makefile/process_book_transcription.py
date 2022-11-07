# Removes the gutenberg header and footer of the transcription file
# And removes the line endings that are not meant to be paragraphs
import json
import sys
import re
import os

def remove_simple_paragraphs(txt):
    return (txt
        .replace("\r\n\r\n", "?!THISISESCAPE_BALTA_PG_MIRO!?")
        .replace("\r\n", " ")
        .replace("?!THISISESCAPE_BALTA_PG_MIRO!?", "\r\n")
    )

def process_book_txt(text, book_id):
    ogtext = text
    text = re.split(r'\*\*\*\s?START[^*]*\*\*\*\s', text, maxsplit=1)
    if len(text) != 2:
        print(f"❌ Book {book_id} has no start of the project gutenberg ebook", file=sys.stderr)
        return ogtext

    text = text[1]
    text = re.split(r'\*\*\*\s?END[^*]*\*\*\*\s', text, maxsplit=1)
    if len(text) != 2:
        print(f"❌ Book {book_id} has no end of the project gutenberg ebook", file=sys.stderr)
        return ogtext
    text = text[0]
    text = text.strip()
    text = remove_simple_paragraphs(text)
    
    return text

for idx, file in enumerate(os.listdir(sys.argv[1])):
    print(f"{idx + 1} Processing transcription for: {file}", file=sys.stderr)
    with open(f"{sys.argv[1]}/{file}", "r+") as f:
        data = json.load(f)
        data['text'] = process_book_txt(data['text'], data['id'])
        f.seek(0)
        json.dump(data, f)
        f.truncate()
