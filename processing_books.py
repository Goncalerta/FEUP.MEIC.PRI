import json
import os

def remove_simple_paragraphs(txt):
    return (txt
        .replace("\r\n\r\n", "?!THISISESCAPE_BALTA_PG_MIRO!?")
        .replace("\r\n", " ")
        .replace("?!THISISESCAPE_BALTA_PG_MIRO!?", "\r\n")
    )

for idx, file in enumerate(os.listdir("output/books")):
    print(f"{idx}/8000 Processing file: {file}")
    with open("output/books/" + file, "r+") as f:
        data = json.load(f)
        data['text'] = remove_simple_paragraphs(data['text'])
        f.seek(0)
        json.dump(data, f)
        f.truncate()

