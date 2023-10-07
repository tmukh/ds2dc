import os
import subprocess

def run_docker_compose(paths):
    if isinstance(paths, str):
        paths = [paths]  # Convert a single string to a list with one element

    for path in paths:
        # Check if the path exists
        if not os.path.exists(path):
            print(f"Path '{path}' does not exist.")
            continue
        
        # Check if it's a directory
        if not os.path.isdir(path):
            print(f"'{path}' is not a directory.")
            continue

        # Change the current working directory to the specified path
        os.chdir(path)
        
        # Run 'docker-compose up' in the current directory
        os.system("docker compose up")

