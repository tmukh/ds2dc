import os
from conversion_scripts import TabularConvert, graphConvert, convertKeyValue
from concurrent.futures import ThreadPoolExecutor
import time
import threading
import fill_json

def convert_files(paths, extension_type, extension_list):
    if extension_type not in ['tabular', 'graph', 'keyvalue', 'nosql']:
        raise ValueError("Invalid extension type. Supported types: 'tabular', 'graph', 'keyvalue', 'nosql'")

    target_extensions = extension_list
    start_time = time.time()  # Record start time

    for path in paths:
        if os.path.isdir(path):
            with ThreadPoolExecutor() as executor:
                for root, _, files in os.walk(path):
                    for file in files:
                        file_extension = os.path.splitext(file)[-1]
                        if file_extension in target_extensions:
                            input_file = os.path.join(root, file)
                            executor.submit(convert_file, input_file, extension_type)
        elif os.path.isfile(path):
            file_extension = os.path.splitext(path)[-1]
            if file_extension in target_extensions:
                input_file = path
                convert_file(input_file, extension_type)
        else:
            print(f"Invalid path: {path}")

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time

    print("Execution time:", elapsed_time, "seconds")
    print("Thread count:", threading.active_count())

def get_output_extension(extension_type):
    if extension_type == 'tabular':
        return '.csv'
    elif extension_type == 'graph':
        return '.graphml'
    elif extension_type == 'keyvalue':
        return '.json'
    else:
        raise ValueError("Invalid extension type. Supported types: 'tabular', 'graph', 'keyvalue', 'nosql'")

def convert_file(input_file, extension_type):
    if extension_type == 'tabular':
        print('in convert')
        convert_to_csv(input_file)
        fill_json.add_files_to_json('csvs',extension_type)

        
    elif extension_type == 'graph':
        convert_to_graphml(input_file)
        fill_json.add_files_to_json('graphs',extension_type)
    elif extension_type == 'keyvalue':
        convert_to_json(input_file)
        fill_json.add_files_to_json('kv_files',extension_type)

def convert_to_csv(input_file):
    TabularConvert.convert_to_csv_s(input_file)

def convert_to_graphml(input_file):
    graphConvert.convert_to_graphml(input_file)

def convert_to_json(input_file):
    convertKeyValue.convert_to_json(input_file)
