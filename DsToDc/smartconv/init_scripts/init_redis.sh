#!/bin/bash

# Check if the flag file exists
if [ ! -f "/kv_files/init_flag" ]; then
  # Commands to run only on the first startup
  redis-server &
  sleep 5
  chmod +x /docker-entrypoint-initdb.d/import.sh
  /docker-entrypoint-initdb.d/import.sh
  echo 'aaa'

  # Create the flag file to indicate commands have been run
  touch "/kv_files/init_flag"
fi

# Start the tail process to keep the container running
tail -f /dev/null

