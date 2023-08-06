import os
import json
import yaml
import xml.etree.ElementTree as ET
from configparser import ConfigParser
import shutil

def get_unique_file_name(output_folder, base_name):
    counter = 1
    file_name = os.path.splitext(base_name)[0]  # Remove the extension from the file name
    file_ext = os.path.splitext(base_name)[1]
    unique_file_name = f"{file_name}{file_ext}"

    while os.path.exists(os.path.join(output_folder, unique_file_name)):
        unique_file_name = f"{file_name}_{counter}{file_ext}"
        counter += 1

    return unique_file_name

def process_json(data, prefix='', txt_file=None, key_set=None, parent_folder_name=None, file_name=None):
    if key_set is None:
        key_set = set()

    if isinstance(data, list):
        for index, value in enumerate(data):
            new_prefix = f"{prefix}_{index}"
            process_json(value, new_prefix, txt_file, key_set, parent_folder_name, file_name)
    elif isinstance(data, dict):
        for key, value in data.items():
            new_key = key.replace(' ', '_')  # Replace spaces with underscores
            if new_key in key_set:
                counter = 1
                while f"{new_key}_{counter}" in key_set:
                    counter += 1
                new_key = f"{new_key}_{counter}"
            key_set.add(new_key)
            new_prefix = f"{prefix}_{new_key}"
            process_json(value, new_prefix, txt_file, key_set, parent_folder_name, file_name)
    else:
        if parent_folder_name and file_name:
            txt_file.write(f"SET {parent_folder_name}_{os.path.splitext(file_name)[0]}_{prefix} {data}\n")  # Remove the extension from the file name

def convert_to_json_and_txt(file_path, output_folder_name):
    if output_folder_name not in ['doc', 'kv_files']:
        raise ValueError("Invalid output folder name. Expected 'doc' or 'kv_files'.")

    output_folder = 'doc_files' if output_folder_name == 'doc' else 'kv_files'

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Supported file extensions and corresponding conversion functions
    conversion_map = {
        '.json': json.load,
        '.yaml': yaml.safe_load,
        '.yml': yaml.safe_load,
        '.xml': lambda file: {child.tag: child.text for child in ET.parse(file).getroot().iter()},
        '.properties': lambda file: {section: dict(ConfigParser().read(file).items(section)) for section in ConfigParser().sections()}
    }

    # Get the file extension
    file_ext = os.path.splitext(file_path)[1].lower()

    # Convert supported file types to JSON
    if file_ext in conversion_map:
        conversion_func = conversion_map[file_ext]
        with open(file_path, 'r') as file:
            data = conversion_func(file)
        base_name = os.path.basename(file_path)
        unique_file_name = get_unique_file_name(output_folder, base_name)
        output_path = os.path.join(output_folder, unique_file_name)
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Call the process_json function for JSON to TXT conversion
        txt_output_folder = 'kv_files'
        if not os.path.exists(txt_output_folder):
            os.makedirs(txt_output_folder)
        txt_output_path = os.path.join(txt_output_folder, 'keys.txt')

        if not os.path.exists(txt_output_path):
            with open(txt_output_path, 'w'):
                pass

        with open(txt_output_path, 'r') as txt_file:
            existing_keys = set(txt_file.read().splitlines())

        with open(txt_output_path, 'a') as txt_file:
            parent_folder_name = os.path.basename(os.path.dirname(file_path))
            process_json(data, txt_file=txt_file, key_set=existing_keys, parent_folder_name=parent_folder_name, file_name=base_name)
    elif file_ext in ['.csv', '.tsv']:
        # Copy the CSV/TSV file to the output folder
        base_name = os.path.basename(file_path)
        unique_file_name = get_unique_file_name(output_folder, base_name)
        output_path = os.path.join(output_folder, unique_file_name)
        shutil.copyfile(file_path, output_path)
    else:
        raise ValueError("Unsupported file type. Only JSON, YAML, XML, Properties, CSV, and TSV files are supported.")
