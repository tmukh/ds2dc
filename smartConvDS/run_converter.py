import subprocess
import sys
import os
from Docker_related import docker_composer_run
script_dir = os.path.abspath(os.path.dirname(__file__))
paths = ""

def check_and_install_arc():
    # Check if 'arc' command is available
    try:
        subprocess.run(['arc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("'arc' is already installed!")
    except Exception:
        print("'arc' is not installed. Installing...")
        # Run your installation script here
        subprocess.run([os.path.join(script_dir, 'init_scripts', 'init_arc.sh')], shell=True)

def run_converter_with_args(model, paths):
    print(script_dir)
    os.chdir(script_dir)

    # Ensure paths is a list
    if isinstance(paths, str):
        paths = [paths]

    # Construct the command to call main.py
    cmd = ['python3', 'main.py', model] + paths
    
    print(cmd)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
        sys.exit(1)

def main():
    check_and_install_arc() 
    if len(sys.argv) < 2:
        print("Invalid Arguments, usage: python -m run_converter <Data Model> <Root folder>")
        sys.exit(1)

    model = sys.argv[1].lower()
    
    if model == 'multiarc':
        paths = input("Enter paths separated by spaces: ").split()
        run_converter_with_args(model, paths)
        docker_composer_run.run_docker_compose(paths.split())
    else:
        root_folder = sys.argv[-1]
        paths = root_folder
        run_converter_with_args(model, paths)
        docker_composer_run.run_docker_compose(paths.split())
if __name__ == "__main__":
    main()
