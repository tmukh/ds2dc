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
    
    converted_paths = []

    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_extension = os.path.splitext(file)[-1]
                    if file_extension in target_extensions:
                        input_file = os.path.join(root, file)
                        converted_file = modify_extension(input_file, output_extension)
                        converted_paths.append(converted_file)
                        convert_file(input_file, extension_type)
        elif os.path.isfile(path):
            file_extension = os.path.splitext(path)[-1]
            if file_extension in target_extensions:
                input_file = path
                converted_file = modify_extension(input_file, output_extension)
                converted_paths.append(converted_file)
                convert_file(input_file, extension_type)
        else:
            print(f"Invalid path: {path}")

    print(converted_paths)
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
    


