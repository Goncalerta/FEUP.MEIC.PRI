precreate-core books

cp /data/enumsConfig.xml /var/solr/data/books/enumsConfig.xml

# Start Solr in background mode so we can use the API to upload the schema
solr start

# Wait for Solr to start
sleep 5
# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary @/data/books_schema.json http://localhost:8983/solr/books/schema
# Wait for Solr to update the schema
sleep 10

# Populate collection
bin/post -c books /data/books/*.xml

# Restart in foreground mode so we can access the interface
solr restart -f