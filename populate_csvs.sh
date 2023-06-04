#!/bin/bash

# Set your PostgreSQL environment variables
PGHOST="localhost"
PGPORT="5432"
PGDATABASE="csvs"
PGUSER="postgres"
PGPASSWORD="postgres"

# Folder path containing CSV files
CSV_FOLDER="/csvs/"

# Loop through all CSV files in the folder
for csv_file in "$CSV_FOLDER"/*.csv; do
    # Extract file name without extension
    filename=$(basename "$csv_file" .csv)

    # Extract headers from the CSV file
    headers=$(head -n 1 "$csv_file" | tr ',' '\n')

    # Generate the CREATE TABLE statement dynamically
    table_name="${filename}_table"
    columns=$(echo "$headers" | awk '{ printf "%s VARCHAR(255),", $0 }' | sed 's/,$//')
    create_table_sql="CREATE TABLE $table_name ($columns);"

    # Execute the CREATE TABLE statement with PGPASSWORD
    PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -d "$PGDATABASE" -U "$PGUSER" -c "$create_table_sql"

    # Import the CSV data into the table with PGPASSWORD
    PGPASSWORD="$PGPASSWORD" psql -h "$PGHOST" -p "$PGPORT" -d "$PGDATABASE" -U "$PGUSER" -c "\copy $table_name FROM '$csv_file' WITH (FORMAT CSV, HEADER TRUE)"

    echo "Table $table_name created successfully and CSV data imported."
done
