#!/bin/bash

precreate-core books

# Start Solr in background mode so we can use the API to upload the schema
sed -i $'/<\/config>/{e cat config.xml\n}' /var/solr/data/books/conf/solrconfig.xml

solr start -Dsolr.ltr.enabled=true

cp /data/synonyms.txt /var/solr/data/books/conf

cp /models/en-ner-person.bin /var/solr/data/books/conf/en-ner-person.bin

cp /models/en-ner-location.bin /var/solr/data/books/conf/en-ner-location.bin

cp /models/en-ner-date.bin /var/solr/data/books/conf/en-ner-date.bin

cp /models/en-sent.bin /var/solr/data/books/conf/en-sent.bin

cp /models/en-token.bin /var/solr/data/books/conf/en-token.bin

cp /models/en-chunker.bin /var/solr/data/books/conf/en-chunker.bin

cp /models/en-pos-maxent.bin /var/solr/data/books/conf/en-pos-maxent.bin

# Wait for Solr to start
sleep 20

# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary @/data/books_schema.json http://localhost:8983/solr/books/schema

# Wait for Solr to update the schema
sleep 10

# Populate collection
bin/post -c books /data/books/*.json

# Restart in foreground mode so we can access the interface
solr restart -f