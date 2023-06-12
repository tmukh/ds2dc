import os
import TabularConvert
import graphConvert
import convertKeyValue
from concurrent.futures import ThreadPoolExecutor
import time
import threading

def convert_files(paths, extension_type, extension_list):
    if extension_type not in ['tabular', 'graph', 'keyvalue', 'nosql']:
        raise ValueError("Invalid extension type. Supported types: 'tabular', 'graph', 'keyvalue', 'nosql'")

    target_extensions = extension_list
    output_extension = get_output_extension(extension_type)

    start_time = time.time()  # Record start time

    for path in paths:
        if os.path.isdir(path):
            with ThreadPoolExecutor() as executor:
                for root, dirs, files in os.walk(path):
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
        convert_to_csv(input_file)
    elif extension_type == 'graph':
        convert_to_graphml(input_file)
    elif extension_type == 'keyvalue':
        convert_to_json(input_file)

def convert_to_csv(input_file):
    TabularConvert.convert_to_csv_s(input_file)

def convert_to_graphml(input_file):
    graphConvert.convert_to_graphml(input_file)

def convert_to_json(input_file):
    convertKeyValue.convert_to_json(input_file)
