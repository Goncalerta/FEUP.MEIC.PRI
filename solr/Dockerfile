FROM solr:8.10

ADD merge /data/books

ADD models /models

COPY config.xml /data/config.xml

COPY enumsConfig.xml /data/enumsConfig.xml

COPY books_schema.json /data/books_schema.json

COPY books_schema_syn.json /data/books_schema_syn.json

COPY synonyms.txt /data/synonyms.txt

COPY startup_nlp.sh /scripts/startup_nlp.sh

ENTRYPOINT ["/scripts/startup_nlp.sh"]