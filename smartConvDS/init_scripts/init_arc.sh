#!/bin/bash
  sudo apt update
  sudo apt install -y wget libicu-dev git

  wget https://github.com/nfdi4plants/arcCommander/releases/download/v0.4.0-linux.x64/arc
  chmod u+x arc
  sudo mv arc /usr/local/bin/
  arc --version


  sudo apt install -y git-lfs
  git lfs install

