FROM solr:8.10

COPY books.json /data/books.json

COPY books_schema.json /data/books_schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]
