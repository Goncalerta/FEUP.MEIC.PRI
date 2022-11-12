cd solr

docker build . -t book_characterization

docker run -p 8983:8983 book_characterization