#!/bin/bash

if [ "$SOLR_SYS" == "BASIC" ]
then
    echo "Using basic Solr system"
fi
if [ "$SOLR_SYS" == "SYN" ]
then
    echo "Using Solr system with synonyms"
fi
if [ "$SOLR_SYS" == "NLP" ]
then
    echo "Using NLP Solr system"
fi
if [ "$SOLR_SYS" == "" ]
then
    echo "No Solr system specified, using basic"
    SOLR_SYS="BASIC"
fi
if [ "$SOLR_SYS" != "BASIC" ] && [ "$SOLR_SYS" != "SYN" ] && [ "$SOLR_SYS" != "NLP" ]
then
    echo "Invalid Solr system specified"
    exit 1
fi

precreate-core books

cp /data/enumsConfig.xml /var/solr/data/books/enumsConfig.xml

if [ "$SOLR_SYS" == "SYN" ] || [ "$SOLR_SYS" == "NLP" ]
then
    cp /data/synonyms.txt /var/solr/data/books/conf
fi

if [ "$SOLR_SYS" == "BASIC" ] || [ "$SOLR_SYS" == "SYN" ]
then
    # Start Solr in background mode so we can use the API to upload the schema
    solr start

    # Wait for Solr to start
    sleep 5
fi

if [ "$SOLR_SYS" == "NLP" ]
then
    # Start Solr in background mode so we can use the API to upload the schema
    sed -i $'/<\/config>/{e cat /data/config.xml\n}' /var/solr/data/books/conf/solrconfig.xml
    solr start -Dsolr.ltr.enabled=true

    cp /models/en-ner-person.bin /var/solr/data/books/conf/en-ner-person.bin

    cp /models/en-ner-location.bin /var/solr/data/books/conf/en-ner-location.bin

    cp /models/en-ner-date.bin /var/solr/data/books/conf/en-ner-date.bin

    cp /models/en-sent.bin /var/solr/data/books/conf/en-sent.bin

    cp /models/en-token.bin /var/solr/data/books/conf/en-token.bin

    cp /models/en-chunker.bin /var/solr/data/books/conf/en-chunker.bin

    cp /models/en-pos-maxent.bin /var/solr/data/books/conf/en-pos-maxent.bin

    sleep 20
fi

# Schema definition via API
if [ "$SOLR_SYS" == "BASIC" ]
then
    curl -X POST -H 'Content-type:application/json' --data-binary @/data/books_schema.json http://localhost:8983/solr/books/schema
fi
if [ "$SOLR_SYS" == "SYN" ]
then
    curl -X POST -H 'Content-type:application/json' --data-binary @/data/books_schema_syn.json http://localhost:8983/solr/books/schema
fi
if [ "$SOLR_SYS" == "NLP" ]
then
    curl -X POST -H 'Content-type:application/json' --data-binary @/data/books_schema_nlp.json http://localhost:8983/solr/books/schema
fi

# Wait for Solr to update the schema
sleep 10

# Populate collection
bin/post -c books /data/books/*.xml

# Restart in foreground mode so we can access the interface
solr restart -f