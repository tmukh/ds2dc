#!/bin/bash

# Function to check if PostgreSQL server is already running
check_postgres_running() {
  pg_isready >/dev/null 2>&1
  return $?
}

# Function to check if PostgreSQL server is ready
check_postgres() {
  until check_postgres_running
  do
    echo "Waiting for PostgreSQL server to start..."
    sleep 1
  done
}

# Call the function to check if PostgreSQL server is ready
check_postgres

# Import CSV files
for file in /csvs/*.csv
do
    # Get the file name without extension
    filename=$(basename "$file" .csv)

    # Create the table name dynamically based on the file name
    table_name="$filename"

    # Read the first line of the CSV file to extract column names
    IFS=, read -r -a columns < "$file"

    # Create the table with the dynamically generated column names
    create_table_query="CREATE TABLE IF NOT EXISTS $table_name ("
    for column in "${columns[@]}"
    do
        create_table_query+="\"$column\" text,"
    done
    create_table_query=${create_table_query%?} # Remove the trailing comma
    create_table_query+=")"

    # Execute the create table query
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "$create_table_query"

    # Import the data from the CSV file into the table
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "COPY $table_name FROM '/csvs/$filename.csv' DELIMITER ',' CSV HEADER"
done
