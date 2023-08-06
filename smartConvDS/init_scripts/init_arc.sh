#!/bin/bash

# Check if the flag file exists
if [ ! -f "/arc_files/init_flag" ]; then
  # Commands to run only on the first startup
  apt update
  apt install -y wget libicu-dev git

  wget https://github.com/nfdi4plants/arcCommander/releases/download/v0.4.0-linux.x64/arc
  chmod u+x arc
  mv arc /usr/local/bin/
  arc --version


  apt install -y git-lfs
  git lfs install


  cd arc_files
  arc export > metadata.json

  # Create the flag file to indicate commands have been run
  touch "/arc_files/init_flag"
fi

# Start the tail process to keep the container running
tail -f /dev/null
