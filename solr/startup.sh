#!/bin/bash

precreate-core books
precreate-core books_syn

cp /data/enumsConfig.xml /var/solr/data/books/enumsConfig.xml
cp /data/enumsConfig.xml /var/solr/data/books_syn/enumsConfig.xml
cp /data/synonyms.txt /var/solr/data/books_syn/conf

# Start Solr in background mode so we can use the API to upload the schema
solr start

# Wait for Solr to start
sleep 5

# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary @/data/books_schema.json http://localhost:8983/solr/books/schema
#curl -X POST -H 'Content-type:application/json' --data-binary @/data/books_schema_syn.json http://localhost:8983/solr/books_syn/schema

# Wait for Solr to update the schema
sleep 10

# Populate collection
bin/post -c books /data/books/*.xml

# Populate collection
#bin/post -c books_syn /data/books/*.xml

# Restart in foreground mode so we can access the interface
solr restart -f