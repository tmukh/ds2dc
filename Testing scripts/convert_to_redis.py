import os
import json

def process_json_files(folder_path):
    data = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as json_file:
                try:
                    json_data = json.load(json_file)
                    for key, value in json_data.items():
                        if key in data:
                            data[key].append(value)
                        else:
                            data[key] = [value]
                except json.JSONDecodeError:
                    print(f"Error parsing JSON file: {file_path}")
    return data

def write_data_file(data, output_file):
    with open(output_file, 'w') as file:
        for key, values in data.items():
            for value in values:
                file.write(f"SET {key} {value}\n")

if __name__ == '__main__':
    folder_path = 'data'  # Folder name changed to 'data'
    output_file = 'data.txt'

    json_data = process_json_files(folder_path)
    write_data_file(json_data, output_file)
