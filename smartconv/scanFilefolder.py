import os
import sys
from generateImage import generate_dockerfile

def traverseSameDataModel(exts, file_paths, model):
    root_folder = os.getcwd()  # Get the root folder path
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if any(file.endswith(ext) for ext in exts):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(
                    file_path, root_folder)  # Get the relative path
                file_paths.append(relative_path.replace("\\", "/"))
    return file_paths
