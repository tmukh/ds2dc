#!/bin/bash

# Check if the flag file exists
if [ ! -f "/docker-entrypoint-initdb.d/init_flag" ]; then
  # Commands to run only on the first startup
  echo "Starting MongoDB..."
  mongod --bind_ip_all &

  # Wait for MongoDB to start
  echo "Waiting for MongoDB to start..."
  sleep 20

  # Import initial data
  echo "Running import script..."
  chmod +x /docker-entrypoint-initdb.d/import.sh
  /docker-entrypoint-initdb.d/import.sh

  # Create the flag file to indicate commands have been run
  echo "Creating init flag..."
  touch "/docker-entrypoint-initdb.d/init_flag"
fi

# Start the tail process to keep the container running
tail -f /dev/null
