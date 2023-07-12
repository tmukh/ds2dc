import yaml
import json
import os

def convert_yaml_to_json(yaml_file, json_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    with open(json_file, 'w') as f:
        json.dump(data, f)
    
    with open(json_file, 'w') as f:
        json.dump(data, f)

def convert_to_document(file_path, output_dir):
    file_extension = os.path.splitext(file_path)[1]

    if file_extension == '.yaml':
        json_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file_path))[0] + '.json')
        convert_yaml_to_json(file_path, json_file)
        print(f'Converted {file_path} to {json_file}')
    elif file_extension == '.json':
        # The file is already in JSON format, so no conversion is needed
        json_file = file_path
        print(f'File {file_path} is already in JSON format')
    else:
        print(f'Unsupported file format: {file_extension}')

# Example usage
output_directory = 'documents'  # Replace with the desired output directory
