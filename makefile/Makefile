
run:
	mkdir -p output/debug/books
	mkdir -p output/debug/reviews
	python fetch_book_ids.py 12000 \
	| python fetch_book_table.py \
	| python filter_duplicates.py \
	| python expect_exactly_one.py 'Title' 'Language' 'Release Date' 'Copyright Status' \
	| python filter_by.py 'Copyright Status' 'Public domain in the USA.' \
	| python filter_by.py 'Language' 'English' \
	| python parse_book_info.py \
	| head -8000 \
	> output/debug/books.jsonl
	python fetch_book_transcription.py "output/debug/books" < output/debug/books.jsonl
	python process_book_transcription.py "output/debug/books"
	python fetch_book_reviews.py "output/debug/reviews" < output/debug/books.jsonl

install:
	apt-get install python-is-python3
	python -m pip install bs4 whoswho selenium requests 
