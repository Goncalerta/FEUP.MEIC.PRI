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

# - The first two scripts respectively fetch and process the book transcriptions from Project Gutenberg
# The processing step of each transcription file consists of removing the Project Gutenberg 
# header and footer that is not part of the transcription, removing single newlines (which)
# are not intended as paragraphs, and substituting double newlines with single newlines (which
# are meant as a single paragraph)
# - The last script fetches the global ratings for the books from Goodreads
output/books: output/books_info.jsonl output/goodreads_ids.csv
	mkdir -p output/books
	python fetch_book_transcription.py "output/books" < output/books_info.jsonl
	python process_book_transcription.py "output/books"
	python fetch_goodreads_ratings.py "output/books" "geckodriver" < output/goodreads_ids.csv

# Fetches the book reviews from Goodreads
output/reviews: output/goodreads_ids.csv
	mkdir -p output/reviews
	python fetch_goodreads_reviews.py "output/reviews" "geckodriver" < output/goodreads_ids.csv

# Fetches, filters and processes the book information from Project Gutenberg
# - fetch_book_ids.py fetches the book ids from the catalog of Project Gutenberg, returning an id for each line
# - fetch_book_table.py fetches the book information for each book id, returning a json object for each line
# (if an improved version of the book is detected during the fetch, the improved version is fetched instead)
# - filter_duplicates.py detects if two instances with different ids refer to the same book (different versions), only printing the first one
# - expect_exactly_one.py filters out the json objects that don't have the fields given by the command arguments or where some of those fields have multiple values
# Each book should have exactly one title, language, release date and copyright status
# - filter_by.py filters out json objects where the given field doesn't have the given value
# Each book should be in english and in public domain in the USA
# - clean_book_info.py cleans the json objects, keeping only relevant fields
# - head is used to limit the number of books to NUM_BOOKS_FINAL
output/books_info.jsonl:
	mkdir -p output
	python fetch_book_ids.py ${NUM_BOOKS_INITIAL_FETCH} \
	| python fetch_book_table.py \
	| python filter_duplicates.py \
	| python expect_exactly_one.py 'Title' 'Language' 'Release Date' 'Copyright Status' \
	| python filter_by.py 'Copyright Status' 'Public domain in the USA.' \
	| python filter_by.py 'Language' 'English' \
	| python clean_book_info.py \
	| head -${NUM_BOOKS_FINAL} \
	> output/books_info.jsonl

# Temporary helper file that translates the book ids to goodreads ids in order to ease
# the process of fetching goodreads.
output/goodreads_ids.csv: output/books_info.jsonl
	python find_goodreads_ids.py < output/books_info.jsonl > output/goodreads_ids.csv

# Installs required dependencies to run the scripts
install: geckodriver
	python -m pip install bs4 whoswho selenium requests 

# Installs geckodriver driver for selenium
geckodriver: 
	wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
	sh -c 'tar -x geckodriver -zf geckodriver-v0.31.0-linux64.tar.gz -O > geckodriver'
	chmod +x geckodriver
	rm geckodriver-v0.31.0-linux64.tar.gz

# Removes the outputs produced in a previous run and the geckodriver binary
clean:
	rm -r output
	rm geckodriver
