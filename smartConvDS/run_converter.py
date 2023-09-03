import subprocess
import sys
import os

script_dir = os.path.abspath(os.path.dirname(__file__))

def check_and_install_arc():
    # Check if 'arc' command is available
    try:
        subprocess.run(['arc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("'arc' is already installed!")
    except Exception:
        print("'arc' is not installed. Installing...")
        # Run your installation script here
        subprocess.run([os.path.join(script_dir, 'init_scripts', 'init_arc.sh')], shell=True)

def run_converter_with_args(model, root_folder):
    print(script_dir)
    os.chdir(script_dir)

    # Construct the command to call main.py
    cmd = ['python3', 'main.py', model, root_folder]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
        sys.exit(1)

def main():
    check_and_install_arc() 
    if len(sys.argv) < 3:
        print("Invalid Arguments, usage: python -m run_converter <Data Model> <Root folder>")
        sys.exit(1)

    model = sys.argv[1].lower()
    root_folder = sys.argv[-1]

    run_converter_with_args(model, root_folder)

if __name__ == "__main__":
    main()
