import os, time, threading
from  conversion_scripts import TabularConvert, graphConvert, convertDocKV
from concurrent.futures import ThreadPoolExecutor
from Testing import convert_to_redis
from  Docker_related import fill_json

def convert_files(paths, extension_type, extension_list, root_folder):
    if extension_type not in ['tabular', 'graph', 'keyvalue', 'document']:
        raise ValueError("Invalid extension type. Supported types: 'tabular', 'graph', 'keyvalue', 'document'")
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
                            executor.submit(convert_file, input_file, extension_type,root_folder)
        elif os.path.isfile(path):
            file_extension = os.path.splitext(path)[-1]
            if file_extension in target_extensions:
                input_file = path
                convert_file(input_file, extension_type, root_folder)
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
    elif extension_type == 'document':
        return '.json'
    else:
        raise ValueError("Invalid extension type. Supported types: 'tabular', 'graph', 'keyvalue', 'document'")
def convert_file(input_file, extension_type, root_folder):
    if extension_type == 'tabular':
        convert_to_csv(input_file, root_folder)
    elif extension_type == 'graph':
        convert_to_graphml(input_file),root_folder
    elif extension_type == 'keyvalue':
        convert_to_json(input_file,root_folder)
    elif extension_type == 'document':
        convert_to_json_doc(input_file,root_folder)

def convert_to_csv(input_file, root_folder):
    TabularConvert.convert_to_csv_s(input_file, root_folder)

def convert_to_graphml(input_file,root_folder):
    graphConvert.convert_to_graphml(input_file, root_folder)

def convert_to_json(input_file,root_folder):
    convertDocKV.convert_to_json(input_file,'kv_files', root_folder)
    convert_to_redis.json_to_txt(input_file)
def convert_to_json_doc(input_file,root_folder):
    convertDocKV.convert_to_json(input_file,'doc', root_folder)
    
