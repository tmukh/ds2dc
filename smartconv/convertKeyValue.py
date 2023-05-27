import os
import json
import yaml
import xml.etree.ElementTree as ET
from configparser import ConfigParser

def convert_to_json(file_path):
    def convert_json(file_path, output_folder):
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        base_name = os.path.basename(file_path)
        output_path = os.path.join(output_folder, f'{os.path.splitext(base_name)[0]}.json')
        
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

    def convert_yaml(file_path, output_folder):
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        
        base_name = os.path.basename(file_path)
        output_path = os.path.join(output_folder, f'{os.path.splitext(base_name)[0]}.json')
        
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

    def convert_xml(file_path, output_folder):
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = {child.tag: child.text for child in root.iter()}
        
        base_name = os.path.basename(file_path)
        output_path = os.path.join(output_folder, f'{os.path.splitext(base_name)[0]}.json')
        
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

    def convert_properties(file_path, output_folder):
        config = ConfigParser()
        config.read(file_path)
        data = {section: dict(config.items(section)) for section in config.sections()}
        
        base_name = os.path.basename(file_path)
        output_path = os.path.join(output_folder, f'{os.path.splitext(base_name)[0]}.json')
        
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)

    # Main code
    
    output_folder = 'keyValue files'

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Supported file extensions and corresponding conversion functions
    conversion_map = {
        '.json': convert_json,
        '.yaml': convert_yaml,
        '.yml': convert_yaml,
        '.xml': convert_xml,
        '.properties': convert_properties
    }

    # Get the file extension
    file_ext = os.path.splitext(file_path)[1].lower()

    # Convert supported file types to JSON
    if file_ext in conversion_map:
        conversion_func = conversion_map[file_ext]
        conversion_func(file_path, output_folder)
