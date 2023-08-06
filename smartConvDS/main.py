import os
import sys
from Crawler import scanFilefolder, checkArcConstraints
from Docker_related import generateImage
from conversion_scripts import convert, arcFileCopy
import run_converter

def get_root_folder():
    return sys.argv[-1]

def handle_command_line_args():
    if len(sys.argv) == 1 or len(sys.argv) > 4:
        print("Invalid Arguments, usage: python convert.py <Data Model> [Root folder]")
        sys.exit(1)

def main():
    handle_command_line_args()
    
    root_folder = get_root_folder()
    model = sys.argv[1].lower()
    
    if not os.path.exists(root_folder):
        print("Error: The specified root folder does not exist.")
        sys.exit(1)
    
    os.chdir(root_folder)
    
    if model == "multimodel":
        multimodel_handler()
    elif model == "domain-specific":
        domain_specific_handler(root_folder)
    elif model in ["tabular", "graph", "keyvalue", "document"]:
        same_datamodel_handler(model, root_folder)
    else:
        print("Invalid Data Model. Available options are: multimodel, domain-specific, same-datamodel [tabular, graph, keyvalue, document]")
        sys.exit(1)

def multimodel_handler():
    exts_dict = {
        "tabular": [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"],
        "graph": [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"],
        "keyvalue": [".json", ".yaml", ".xml", ".properties"],
        "document": [".json", ".bson", ".yaml", ".csv", ".tsv"]
    }

    all_paths = []
    for model in exts_dict:
        paths = scanFilefolder.traverseSameDataModel(exts_dict[model])
        all_paths.extend(paths)
        convert.convert_files(paths, model, exts_dict[model])

    dockerfiles = generateImage.generate_docker_compose(all_paths, 'multimodel', [])

def domain_specific_handler(root_folder):
    os.chdir(root_folder)
    arc_paths = scanFilefolder.traverseDomainSpecific([".csv", ".tsv", ".json", ".txt"])
    if checkArcConstraints.check_folder_structure(root_folder):
        print("arc structure valid!")
        arcFileCopy.copy_files_to_arc_folder(arc_paths)
        run_converter.run_converter_with_args('multimodel', root_folder)
        os.chdir(root_folder)
        dockerfiles = generateImage.generate_docker_compose(arc_paths, "domain-specific", root_folder)
    else:
        print('invalid structure')
        sys.exit(1)

def same_datamodel_handler(model, root_folder):
    exts_dict = {
        "tabular": [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"],
        "graph": [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"],
        "keyvalue": [".json", ".yaml", ".xml", ".properties"],
        "document": [".json", ".bson", ".yaml", ".csv", ".tsv"]
    }

    exts = exts_dict.get(model.lower())
    if not exts:
        print(f"Invalid Data Model. Available options for same-datamodel are: {', '.join(exts_dict.keys())}")
        sys.exit(1)

    paths = scanFilefolder.traverseSameDataModel(exts)
    convert.convert_files(paths, model, exts)
    dockerfiles = generateImage.generate_docker_compose(paths, model, [])

if __name__ == "__main__":
    main()
