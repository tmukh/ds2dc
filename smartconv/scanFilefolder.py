import os
import sys
from generateImage import generate_dockerfile

def traverseSameDataModel(exts):
    root_folder = os.getcwd()  # Get the root folder path
    file_paths = []
    #NOTE: using os.walk here because it handles recursively checking all the subdirectories
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if any(file.endswith(ext) for ext in exts):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(
                    file_path, root_folder)  # Get the relative path
                file_paths.append(relative_path.replace("\\", "/"))
    return file_paths

def traverseMultiDataModels(exts):
    root_folder = os.getcwd()  # Get the root folder path
    
    # Create three separate lists for each file extension category
    tabular_exts = [".csv", ".xlsx", ".xls", ".tsv",
                    ".parquet", ".feather", ".sqlite", ".db"]
    keyvalue_exts = [".json", ".yaml", ".xml", ".properties"]
    graph_exts = [".graphml", ".gml", ".gexf",
                    ".gdf", ".edgelist", ".adjlist"]
    files_list_1 = []
    files_list_2 = []
    files_list_3 = []

    # NOTE: using os.walk here because it handles recursively checking all the subdirectories
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if any(file.endswith(ext) for ext in tabular_exts):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(
                    file_path, root_folder)  # Get the relative path
                files_list_1.append(relative_path.replace("\\", "/"))
            elif any(file.endswith(ext) for ext in graph_exts):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(
                    file_path, root_folder)  # Get the relative path
                files_list_2.append(relative_path.replace("\\", "/"))
            elif any(file.endswith(ext) for ext in keyvalue_exts):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(
                    file_path, root_folder)  # Get the relative path
                files_list_3.append(relative_path.replace("\\", "/"))

    return files_list_1, files_list_2, files_list_3

