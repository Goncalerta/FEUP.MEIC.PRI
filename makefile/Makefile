# The number of books to fetch initially (should be large enough so that there are 
# at least NUM_BOOKS_FINAL after the filtering steps)
NUM_BOOKS_INITIAL_FETCH = 12000 
# The number of books that we intend to end with (only this amount will fetch and 
# process reviews and transcriptions, the two most time-consuming steps in the pipeline)
NUM_BOOKS_FINAL = 8000

# Installs dependencies needed and runs the pipeline
all: install run

# Runs the entire pipeline
run: output/books output/reviews

# Fetches and processes the book transcriptions from Project Gutenberg
# The processing step of each transcription file consists of removing the Project Gutenberg 
# header and footer that is not part of the transcription, removing single newlines (which)
# are not intended as paragraphs, and substituting double newlines with single newlines (which
# are meant as a single paragraph)
output/books: output/books_info.jsonl
	mkdir -p output/books
	python fetch_book_transcription.py "output/books" < output/books_info.jsonl
	python process_book_transcription.py "output/books"

# Fetches and processes the book reviews from Goodreads
# TODO @biromiro describe this step (and maybe separate it into multiple steps)
output/reviews: output/books_info.jsonl
	mkdir -p output/reviews
	python fetch_book_reviews.py "output/reviews" < output/books_info.jsonl

# Fetches, filters and processes the book information from Project Gutenberg
# - fetch_book_ids.py fetches the book ids from the catalog of Project Gutenberg, returning an id for each line
# - fetch_book_table.py fetches the book information for each book id, returning a json object for each line
# (if an improved version of the book is detected during the fetch, the improved version is fetched instead)
# - filter_duplicates TODO
output/books_info.jsonl:
	mkdir -p output
	python fetch_book_ids.py ${NUM_BOOKS_INITIAL_FETCH} \
	| python fetch_book_table.py \
	| python filter_duplicates.py \
	| python expect_exactly_one.py 'Title' 'Language' 'Release Date' 'Copyright Status' \
	| python filter_by.py 'Copyright Status' 'Public domain in the USA.' \
	| python filter_by.py 'Language' 'English' \
	| python parse_book_info.py \
	| head -${NUM_BOOKS_FINAL} \
	> output/books_info.jsonl

# Installs required python dependencies to run the scripts
install:
	python -m pip install bs4 whoswho selenium requests 

# Removes the outputs produced in a previous run
clean:
	rm -r output
