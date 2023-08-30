import os, sys

def traverseDataModel(exts, excluded_dirs=None):
    root_folder =  sys.argv[-1] # Get the root folder path
    file_paths = []

    if excluded_dirs is None:
        excluded_dirs = ["csvs", "graphs", "kv_files", "doc_files", ".vscode", "arc_files"]

    excluded_files = ["arcMetadata.json"]  # Add the file you want to exclude

    for root, _, files in os.walk(root_folder):
        if any(dir_name in root for dir_name in excluded_dirs):
            continue

        file_paths.extend(
            os.path.relpath(os.path.join(root, file), root_folder).replace("\\", "/")
            for file in files
            if any(file.endswith(ext) for ext in exts) and file not in excluded_files       )
    print(file_paths)
    return file_paths

def traverseSameDataModel(exts):
    return traverseDataModel(exts)

def traverseMultiDataModels():
    root_folder =  sys.argv[-1] # Get the root folder path

    # Create separate lists for each file extension category
    tabular_exts = [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"]
    keyvalue_exts = [".json", ".yaml", ".xml", ".properties"]
    graph_exts = [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"]
    document_exts = [".json", ".bson", ".yaml", ".csv", ".tsv"]

    files_list_1 = traverseDataModel(tabular_exts, excluded_dirs=["csv", "graphs", "kv_files", "doc_files", ".vscode", "arc_files"])
    files_list_2 = traverseDataModel(graph_exts, excluded_dirs=["csv", "graphs", "kv_files", "doc_files", ".vscode", "arc_files"])
    files_list_3 = traverseDataModel(keyvalue_exts, excluded_dirs=["csv", "graphs", "kv_files", "doc_files", ".vscode", "arc_files"])
    files_list_4 = traverseDataModel(document_exts, excluded_dirs=["csv", "graphs", "kv_files", "doc_files", ".vscode", "arc_files"])

    return files_list_1, files_list_2, files_list_3, files_list_4

def traverseDomainSpecific(exts):
    return traverseDataModel(exts, excluded_dirs=["csv", "graphs", "kv_files", "doc_files", ".vscode", "arc_files"])

def is_readable(file_path):
    try:
        with open(file_path, "r"):
            return True
    except Exception:
        return False
