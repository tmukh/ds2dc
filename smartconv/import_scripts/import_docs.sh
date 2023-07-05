#!/bin/bash

set -e

mongoimport_args="--host localhost --port 27017 --db $MONGO_INITDB_DATABASE --jsonArray"

for dir in /docker-entrypoint-initdb.d/*/
do
    collection=$(basename "$dir")
    for file in "$dir"*.json
    do
        mongoimport $mongoimport_args --collection "$collection" --file "$file"
    done
done
