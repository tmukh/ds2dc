import os
import pandas as pd
import TabularConvert, graphConvert, convertKeyValue
import generateImage
def convert_files(paths, extension_type, extension_list):
    if extension_type not in ['tabular', 'graph', 'keyvalue', 'nosql']:
        raise ValueError("Invalid extension type. Supported types: 'tabular', 'graph', 'keyvalue', 'nosql'")
    
    target_extensions = extension_list
    
    if extension_type == 'tabular':
        output_extension = '.csv'
    elif extension_type == 'graph':
        output_extension = '.graphml'
    elif extension_type == 'keyvalue':
        output_extension = '.json'
    


    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_extension = os.path.splitext(file)[-1]
                    if file_extension in target_extensions:
                        input_file = os.path.join(root, file)
                        convert_file(input_file, extension_type)
        elif os.path.isfile(path):
            file_extension = os.path.splitext(path)[-1]
            if file_extension in target_extensions:
                input_file = path
                convert_file(input_file, extension_type)
        else:
            print(f"Invalid path: {path}")

def get_extension(file_path):
    # Extract the extension from the file path
    parts = file_path.split('.')
    if len(parts) > 1:
        return '.' + parts[-1]
    else:
        return ''
def convert_strings_to_paths(file_paths):
    os_paths = []
    for file_path in file_paths:
        os_path = os.path.normpath(file_path)
        os_paths.append(os_path)
    return file_paths
def convert_files_by_extension(file_paths):

    file_paths = convert_strings_to_paths(file_paths)
    converted_paths = []

    for file_path in file_paths:
        extension = get_extension(file_path)
        exts_tabular = [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"]
        exts_graph = [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"]
        exts_keyvalue = [".json", ".yaml", ".xml", ".properties"]   
        if extension.lower() in exts_tabular:
            convert_to_csv(file_path)
            converted_paths.append(file_path)
        elif extension.lower() in exts_graph:
            convert_to_graphml(file_path)
            converted_paths.append(file_path)
        elif extension.lower() in exts_keyvalue:
            convert_to_json(file_path)
            converted_paths.append(file_path)
        else:
            print(f"Unsupported extension: {extension}")

    return converted_paths


def modify_extension(file_path, new_extension):
    filename, _ = os.path.splitext(file_path)
    return filename + new_extension

def convert_file(input_file, extension_type):
    if extension_type == 'tabular':
        convert_to_csv(input_file)
    elif extension_type == 'graph':
        convert_to_graphml(input_file,)
    elif extension_type == 'keyvalue':
        convert_to_json(input_file,)
        
def convert_to_csv(input_file):
    TabularConvert.convert_to_csv_s(input_file)
    
def convert_to_graphml(input_file):
    graphConvert.convert_to_graphml(input_file)
    
def convert_to_json(input_file):
    convertKeyValue.convert_to_json(input_file)
    


