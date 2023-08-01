import os
import sys
from Crawler import scanFilefolder, checkArcConstraints
import run_converter
from Docker_related import generateImage
from conversion_scripts import convert, arcFileCopy

root_folder = sys.argv[-1]

def get_root_folder():
    return root_folder
def handle_command_line_args():
    if len(sys.argv) == 1 or len(sys.argv) > 4:
        print("Invalid Arguments, usage: python convert.py <Data Model> [Root folder]")
        sys.exit(1)

def main():
    handle_command_line_args()
    
    root_folder = sys.argv[-1]
    model = sys.argv[1].lower()
    
    if not os.path.exists(root_folder):
        print("Error: The specified root folder does not exist.")
        sys.exit(1)
    
    os.chdir(root_folder)
    
    if model == "multimodel":
        multimodel_handler(root_folder)
    elif model == "domain-specific":
        domain_specific_handler(root_folder)
    elif model in ["tabular", "graph", "keyvalue", "document"]:
        same_datamodel_handler(model, root_folder)
    else:
        print("Invalid Data Model. Available options are: multimodel, domain-specific, same-datamodel [tabular, graph, keyvalue, document]")
        sys.exit(1)

def multimodel_handler(root_folder):
    
    exts_tabular = [".csv", ".xlsx", ".xls", ".tsv",
                    ".parquet", ".feather", ".sqlite", ".db"]
    exts_graph = [".graphml", ".gml", ".gexf",
                  ".gdf", ".edgelist", ".adjlist"]
    exts_keyvalue = [".json", ".yaml", ".xml", ".properties"]
    exts_document = [".json", ".bson", ".yaml",".csv", ".tsv"]

    tabular_paths = scanFilefolder.traverseMultiDataModels()[0]
    graph_paths = scanFilefolder.traverseMultiDataModels()[1]
    keyvalue_paths = scanFilefolder.traverseMultiDataModels()[2]
    document_paths = scanFilefolder.traverseMultiDataModels()[3]

    all_paths = [item for sublist in [tabular_paths, graph_paths,
                                      keyvalue_paths, document_paths] for item in sublist]

    # Process tabular files
    convert.convert_files(tabular_paths, "tabular", exts_tabular, root_folder)

    # Process graph files
    convert.convert_files(graph_paths, "graph", exts_graph, root_folder)

    # Process key-value files
    convert.convert_files(keyvalue_paths, "keyvalue", exts_keyvalue, root_folder)

    # Process document files
    convert.convert_files(document_paths, "document", exts_document, root_folder)

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
    convert.convert_files(paths, model, exts, root_folder)
    dockerfiles = generateImage.generate_docker_compose(paths, model, [])

if __name__ == "__main__":
    main()
