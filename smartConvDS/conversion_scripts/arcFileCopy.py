import os
import shutil

def copy_files_to_arc_folder(file_paths):
    # Get the root folder where the script is located
    root_folder = os.getcwd()

    # Create the 'arc' folder in the root folder if it doesn't exist
    arc_folder_path = os.path.join(root_folder, 'arc_files')
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

