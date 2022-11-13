FROM solr:8.10

ADD merge /data/books

COPY enumsConfig.xml /data/enumsConfig.xml

COPY books_schema.json /data/books_schema.json

COPY books_schema_syn.json /data/books_schema_syn.json

COPY synonyms.txt /data/synonyms.txt

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]