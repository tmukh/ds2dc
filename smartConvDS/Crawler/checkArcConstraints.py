import os
import pandas as pd

def check_folder_structure(root_folder):
    required_files = {
        "root": ["isa.investigation.xlsx"],
        "assays": ["isa.assay.xlsx"],
        "runs": ["isa.datapackage.xlsx"],
        "studies": ["isa.study.xlsx"],
    }

    # Check if the root folder exists
    if not os.path.exists(root_folder):
        print(f"Root folder '{root_folder}' not found.")
        return False

    # Check for required files in the root folder
    for file in required_files["root"]:
        file_path = os.path.join(root_folder, file)
        if not os.path.exists(file_path):
            print(f"Required file '{file}' not found in the root folder.")
            return False

    # Check for subfolders
    subfolders = ["assays", "runs", "studies", "workflows"]
    for subfolder in subfolders:
        subfolder_path = os.path.join(root_folder, subfolder)
        if not os.path.exists(subfolder_path):
            print(f"Subfolder '{subfolder}' not found in the root folder.")
            return False

        # Check for assay subfolders and their required files
        if subfolder == "assays":
            assay_folders = [f.name for f in os.scandir(subfolder_path) if f.is_dir()]
            for assay_folder in assay_folders:
                assay_file_path = os.path.join(subfolder_path, assay_folder, "isa.assay.xlsx")
                if not os.path.exists(assay_file_path):
                    print(f"Required file 'isa.assay.xlsx' not found in '{assay_folder}' subfolder.")
                    return False

        # Check for runs subfolders and their required files
        # elif subfolder == "runs":
        #     run_folders = [f.name for f in os.scandir(subfolder_path) if f.is_dir()]
        #     for run_folder in run_folders:
        #         run_file_path = os.path.join(subfolder_path, run_folder, "isa.datapackage.xlsx")
        #         if not os.path.exists(run_file_path):
        #             print(f"Required file 'isa.datapackage.xlsx' not found in '{run_folder}' subfolder.")
        #             return False

        # Check for studies subfolders and their required files
        elif subfolder == "studies":
            study_folders = [f.name for f in os.scandir(subfolder_path) if f.is_dir()]
            for study_folder in study_folders:
                study_file_path = os.path.join(subfolder_path, study_folder, "isa.study.xlsx")
                if not os.path.exists(study_file_path):
                    print(f"Required file 'isa.study.xlsx' not found in '{study_folder}' subfolder.")
                    return False

    return True

