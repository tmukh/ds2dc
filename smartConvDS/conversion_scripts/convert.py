import os
import sys
import time
import re  # Import the regular expression module for sanitization
from conversion_scripts import TabularConvert, graphConvert, convertDocKV, documentConvert
from Testing import convert_to_redis

root_folder = sys.argv[-1]

# Dictionary to map extension types to their corresponding conversion functions
conversion_info = {
    'tabular': (TabularConvert.convert_to_csv_parallel, None),
    'graph': (graphConvert.convert_to_graphml, None),
    'keyvalue': (convertDocKV.convert_to_json_and_txt, 'kv_files'),
    'document': (convertDocKV.convert_to_json_and_txt, 'doc')
}

def sanitize_file_name(file_name):
    # Replace invalid characters with underscores, including hyphens
    return re.sub(r'[^\w_.-]', '_', file_name).replace(' ', '_')


def convert_files(paths, extension_type, extension_list):
    if extension_type not in ['tabular', 'graph', 'keyvalue', 'document']:
        raise ValueError("Invalid extension type. Supported types: 'tabular', 'graph', 'keyvalue', 'document'")
    target_extensions = set(extension_list)
    start_time = time.time()  # Record start time

    for path in paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_extension = os.path.splitext(file)[-1]
                    if file_extension in target_extensions:
                        input_file = os.path.join(root, file)
                        sanitized_file_name = sanitize_file_name(file)  # Sanitize the file name
                        sanitized_input_file = os.path.join(root, sanitized_file_name)
                        os.rename(input_file, sanitized_input_file)  # Rename the file
                        convert_file(sanitized_input_file, extension_type)
        elif os.path.isfile(path):
            file_extension = os.path.splitext(path)[-1]
            if file_extension in target_extensions:
                input_file = path
                sanitized_file_name = sanitize_file_name(os.path.basename(input_file))  # Sanitize the file name
                sanitized_input_file = os.path.join(os.path.dirname(input_file), sanitized_file_name)
                os.rename(input_file, sanitized_input_file)  # Rename the file
                convert_file(sanitized_input_file, extension_type)
        else:
            print(f"Invalid path: {path}")

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time

    print("Execution time:", elapsed_time, "seconds")

def convert_file(input_file, extension_type):
    if extension_type in conversion_info:
        conversion_function, output_folder_name = conversion_info[extension_type]
        if output_folder_name is not None:
            conversion_function(input_file, output_folder_name)
        else:
            conversion_function(input_file)
    else:
        print(f"Invalid extension type: {extension_type}")

        