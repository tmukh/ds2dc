import csv
import os
import json

def add_files_to_json(folder_name, model_type):
    # Load the existing JSON structure from file
    with open('meta-data.json', 'r') as json_file:
        json_data = json.load(json_file)
    # Remove existing tables and relationships based on model type
    if model_type != 'tabular':
        json_data['schemas'][0]['tables'] = [table for table in json_data['schemas'][0]['tables'] if table['type'] == 'custom' and table['factory'] != 'TabularFactory']
    if model_type != 'graph':
        json_data['schemas'][0]['tables'] = [table for table in json_data['schemas'][0]['tables'] if table['type'] == 'custom' and table['factory'] != 'GraphFactory']
    if model_type != 'document':
        json_data['schemas'][0]['tables'] = [table for table in json_data['schemas'][0]['tables'] if table['type'] == 'custom' and table['factory'] != 'DocumentFactory']
    if model_type != 'keyvalue':
        json_data['schemas'][0]['tables'] = [table for table in json_data['schemas'][0]['tables'] if table['type'] == 'custom' and table['factory'] != 'KeyValueFactory']

    # Add new files based on the model type
    if model_type == 'tabular':
        for file in os.listdir(folder_name):
            if file.endswith('.csv'):
                file_path = os.path.join(folder_name, file)
                with open(file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    columns = next(csv_reader)  # Read the first line as column names

                table_data = {
                    "type": "tabular",
                    "columns": []
                }

                for column in columns:
                    table_data['columns'].append({
                        "name": column,
                        "type": "VARCHAR"  # Modify the type based on your requirements
                    })

                table_name = file.replace('.csv', '')  # Set table name as the CSV file name without extension

                json_data['schemas'][0]['tables'].append({
                    "name": table_name,
                    "type": "custom",
                    "factory": "TabularFactory",
                    "operand": table_data
                })
    elif model_type == 'graph':
        # Implementation for Graph model
        pass
    elif model_type == 'document':
        # Implementation for Document model
        pass
    elif model_type == 'keyvalue':
        # Implementation for Key Value model
        pass

    # Write the updated JSON structure to a new file
    with open('output_file.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
