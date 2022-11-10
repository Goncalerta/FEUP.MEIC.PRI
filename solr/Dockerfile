FROM solr:8.10

ADD merge /data/books

COPY books_schema.json /data/books_schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]
