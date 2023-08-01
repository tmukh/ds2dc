import subprocess
import sys
import os

script_dir = os.path.abspath(os.path.dirname(__file__))

def run_converter_with_args(model, root_folder):
    script_dir = os.path.abspath(os.path.dirname(__file__))
    print(script_dir)
    os.chdir(script_dir)

    # Construct the command to call main.py
    cmd = ['python', 'main.py', model, root_folder]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Invalid Arguments, usage: python run_converter.py <Data Model> <Root folder>")
        sys.exit(1)

    model = sys.argv[1].lower()
    root_folder = sys.argv[2]

    run_converter_with_args(model, root_folder)

if __name__ == "__main__":
    main()
