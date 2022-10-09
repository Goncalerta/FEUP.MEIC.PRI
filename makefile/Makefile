NUM_BOOKS_INITIAL_FETCH = 12000
NUM_BOOKS_FINAL = 8000

all: install run

run: output/books output/reviews

output/books: output/books_info.jsonl
	mkdir -p output/books
	python fetch_book_transcription.py "output/books" < output/books_info.jsonl
	python process_book_transcription.py "output/books"

output/reviews: output/books_info.jsonl
	mkdir -p output/reviews
	python fetch_book_reviews.py "output/reviews" < output/books_info.jsonl

output/books_info.jsonl:
	mkdir output
	python fetch_book_ids.py ${NUM_BOOKS_INITIAL_FETCH} \
	| python fetch_book_table.py \
	| python filter_duplicates.py \
	| python expect_exactly_one.py 'Title' 'Language' 'Release Date' 'Copyright Status' \
	| python filter_by.py 'Copyright Status' 'Public domain in the USA.' \
	| python filter_by.py 'Language' 'English' \
	| python parse_book_info.py \
	| head -${NUM_BOOKS} \
	> output/books_info.jsonl

install:
	# apt-get install python-is-python3
	python -m pip install bs4 whoswho selenium requests 

clean:
	rm -r output
