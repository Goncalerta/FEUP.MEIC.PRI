import json
import os
import sys
import re
import unicodedata

def split_words(txt):
    encoded_str = unicodedata.normalize('NFD', txt).encode('ascii', 'ignore').decode('ascii')
    encoded_str = re.sub(r"[^a-zA-Z'\s]", ' ', encoded_str).lower()
    return encoded_str.split()

def count_words():
    word_counts = {}
    for idx, file in enumerate(os.listdir("output/books")):
        print(f"{idx}/8000 Processing file: {file}", file=sys.stderr)
        with open("output/books/" + file, "r") as f:
            text = json.load(f)['text']
            word_list = split_words(text)

            for word in word_list:
                word_counts[word] = word_counts.get(word, 0) + 1

    print(f"ALL DONE; NOW SAVING", file=sys.stderr)
    for k, v in word_counts.items():
        print(f"{k},{v}")
    
    print("OVER", file=sys.stderr)

count_words()