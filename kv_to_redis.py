import os
import json
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Read JSON files from directory
json_dir = "/kv_files/"
json_files = [file for file in os.listdir(json_dir) if file.endswith(".json")]

if not json_files:
    print("No JSON files found in the directory.")
    exit(0)

# Import JSON files into Redis
for json_file in json_files:
    with open(os.path.join(json_dir, json_file)) as file:
        json_content = json.load(file)
        if isinstance(json_content, dict):
            # Extract field-value pairs from JSON and import into Redis
            for field, value in json_content.items():
                r.set(field, json.dumps(value))
        elif isinstance(json_content, list):
            # Handle JSON arrays by creating numbered keys in Redis
            for index, item in enumerate(json_content):
                key = f"{json_file}:{index}"
                r.set(key, json.dumps(item))
        else:
            print(f"Unsupported JSON structure in file: {json_file}")
