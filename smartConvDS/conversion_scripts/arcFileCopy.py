import os
import shutil
import subprocess
import re
import main

def copy_files_to_arc_folder(file_paths,root_folder):

    # Create the 'arc' folder in the root folder if it doesn't exist
    arc_folder_path = os.path.join(root_folder, 'arc_files')
    subprocess.run('arc export >> arcMetadata.json', shell=True)
    print(main.get_root_folder())
    sanitizeMetaData(main.get_root_folder()+'/arcMetadata.json')

    if not os.path.exists(arc_folder_path):
        os.makedirs(arc_folder_path)

    for file_path in file_paths:
        try:
            # Get the filename from the file path
            file_name = os.path.basename(file_path)
            # Construct the destination file path in the 'arc' folder
            destination_path = os.path.join(arc_folder_path, file_name)
            # Copy the file to the 'arc' folder
            shutil.copy2(file_path, destination_path)
            print(f"Copied {file_path} to {destination_path}")
        except Exception as e:
            print(f"Error copying {file_path}: {str(e)}")

def sanitizeMetaData(file_path):
    # Specify the path to your input JSON file
    # Read the contents of the file
    with open(file_path, "r") as f:
        content = f.read()

    # Use line breaks to split the content into sections
    sections = content.split("\n")

    # Extract content from each section
    for i, section in enumerate(sections):
        if "{" in section and "}" in section:
            start_index = section.find("{")
            end_index = section.rfind("}")
            extracted_content = section[start_index:end_index + 1]

            output_file_path = f"arcMetadata_{i+1}.json"

            # Write the extracted content to the output file
            with open(output_file_path, "w") as output_file:
                output_file.write(extracted_content)

            print(f"Extracted content {i+1} saved in {output_file_path}")


