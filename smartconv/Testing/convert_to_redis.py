import json
import os


def process_json(data, prefix='', txt_file=None):
    if isinstance(data, list):
        for index, value in enumerate(data):
            new_prefix = f"{prefix}_{index}"
            process_json(value, new_prefix, txt_file)
    elif isinstance(data, dict):
        for key, value in data.items():
            new_key = key.replace(' ', '_')  # Replace spaces with underscores
            new_prefix = f"{prefix}_{new_key}"
            process_json(value, new_prefix, txt_file)
    else:
        txt_file.write(f"SET {prefix} {data}\n")


def json_to_txt(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    output_folder = 'kv_files'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.basename(json_file_path)
    output_path = os.path.join(output_folder, f'{os.path.splitext(base_name)[0]}.txt')

    with open(output_path, 'w') as txt_file:
        process_json(data, txt_file=txt_file)
