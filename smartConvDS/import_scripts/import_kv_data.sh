#!/bin/bash

# Check if redis-cli is installed
if ! command -v redis-cli &> /dev/null; then
    echo "redis-cli not found. Please make sure Redis is installed and in your PATH."
    exit 1
fi

# Directory containing .txt files
folder="/kv_files"

# Change to the directory
cd "$folder" || { echo "Failed to change to $folder"; exit 1; }

# Loop through all .txt files and perform Redis bulk import
find . -maxdepth 1 -type f -name "*.txt" | while IFS= read -r file; do
    echo "Performing Redis bulk import for $file..."
    cat "$file" | redis-cli --pipe
    echo "Done!"
done

echo "All Redis bulk imports completed."
