#!/bin/bash

set -e

mongoimport_args="--host localhost --port 27017 --db $MONGO_INITDB_DATABASE --username admin --password 123 --authenticationDatabase admin"

# Function to import a single CSV file into its own collection
function import_csv_file() {
    local file=$1
    local collection=$(basename "$file" | cut -d. -f1)

    mongoimport $mongoimport_args --type csv --headerline --collection "$collection" --file "$file"
}

# Function to import a single TSV file into its own collection
function import_tsv_file() {
    local file=$1
    local collection=$(basename "$file" | cut -d. -f1)

    mongoimport $mongoimport_args --type tsv --headerline --collection "$collection" --file "$file"
}

# Function to import CSV/TSV files in a directory
function import_csv_files() {
    local dir=$1

    # Check if CSV/TSV files exist in the directory
    csv_files=$(find "$dir" -type f \( -name "*.csv" -o -name "*.tsv" \))
    if [ -n "$csv_files" ]; then
        for file in $csv_files; do
            if [[ "$file" == *.csv ]]; then
                import_csv_file "$file"
            elif [[ "$file" == *.tsv ]]; then
                import_tsv_file "$file"
            fi
        done
    else
        echo "No CSV/TSV files found in directory: $dir"
    fi
}

# Recursively search for JSON files in all subdirectories and import them
find /docker-entrypoint-initdb.d/ -type f -name "*.json" -print0 | while IFS= read -r -d $'\0' json_file; do
    collection=$(basename "$(dirname "$json_file")")

    # Import JSON files
    mongoimport $mongoimport_args --collection "$collection" --file "$json_file"

    # Get the directory path of the JSON file to find CSV/TSV files
    dir=$(dirname "$json_file")

    # Import CSV/TSV files in the same directory if they exist
    import_csv_files "$dir"
done

# Import CSV/TSV files in the root directory if they exist
import_csv_files "/docker-entrypoint-initdb.d"

# Wait for the MongoDB server to start
sleep 5

# Create additional user or perform other initialization tasks if needed
