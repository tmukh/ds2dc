import os
import pandas as pd
import TabularConvert, graphConvert, convertKeyValue
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
    elif extension_type == 'nosql':
        output_extension = '.yaml'
    
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
            
def convert_file(input_file, extension_type):
    if extension_type == 'tabular':
        convert_to_csv(input_file)
    elif extension_type == 'graph':
        print('INPUT FILE IS AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA ',input_file)

        convert_to_graphml(input_file,)
    elif extension_type == 'keyvalue':
        convert_to_json(input_file,)
    elif extension_type == 'nosql':
        convert_to_yaml(input_file)
        
def convert_to_csv(input_file):
    TabularConvert.convert_to_csv_s(input_file)
    
def convert_to_graphml(input_file):
    graphConvert.convert_to_graphml(input_file)
    
    # TODO: Implement the conversion logic
    
def convert_to_json(input_file):
    convertKeyValue.convert_to_json(input_file)
    
def convert_to_yaml(input_file, output_file):
    # Perform conversion logic from NoSQL file to YAML
    print(f"Converting {input_file} to YAML format: {output_file}")
    # TODO: Implement the conversion logic


