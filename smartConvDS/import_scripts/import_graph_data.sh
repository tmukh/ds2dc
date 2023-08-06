#!/bin/bash

# Import graphml files
for file in /var/lib/neo4j/import/graphs/*.graphml; do
    cypher-shell "CALL apoc.import.graphml('$file', {})"
done

# Import CSV files
for file in /var/lib/neo4j/import/csv/*.csv; do
    filename=$(basename "$file")
    extension="${filename##*.}"
    filename="${filename%.*}"
    cypher-shell "LOAD CSV WITH HEADERS FROM 'file:///$(basename "$file")' AS row CREATE (:${filename//[^[:alnum:]_]/'_'} {row})"
done
