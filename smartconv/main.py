import scanFilefolder
from Docker_related import generateImage
import sys
from conversion_scripts import convert

if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print(
            "Invalid Arguments, usage: python convert.py <Data Model> [Extension]")
    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == "multimodel":
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
            convert.convert_files(tabular_paths, "tabular", exts_tabular)

            # Process graph files
            convert.convert_files(graph_paths, "graph", exts_graph)

            # Process key-value files
            convert.convert_files(keyvalue_paths, "keyvalue", exts_keyvalue)

            convert.convert_files(document_paths, "document", exts_document)

            dockerfiles = generateImage.generate_dockerfile(all_paths, 'multimodel')

        elif sys.argv[1].lower() == "domain-specific":
            # Handle domain-specific data model case
            pass
        else:
            print("Invalid Data Model, Data model has to be one of the following:\n"
                  "1. multimodel\n"
                  "2. domain-specific\n"
                  "3. same-datamodel [Extension]\n")
            sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[1].lower() == "same-datamodel":
        model = sys.argv[2].lower()
        if model == "tabular":
            exts = [".csv", ".xlsx", ".xls", ".tsv",
                    ".parquet", ".feather", ".sqlite", ".db"]
        elif model == "graph":
            exts = [".graphml", ".gml", ".gexf",
                    ".gdf", ".edgelist", ".adjlist"]
        elif model == "keyvalue":
            exts = [".json", ".yaml", ".xml", ".properties"]
        elif model == "document":
            exts = [".json", ".bson", ".yaml", ".csv", ".tsv"]
        else:
            print("Invalid Data Model. Available options for same-datamodel are: tabular, graph, keyvalue, document")
            sys.exit(1)

        paths = scanFilefolder.traverseSameDataModel(exts)

        if model == "tabular":
            has_header = input("Does the CSV file have a header? (y/n): ")
            if has_header.lower() != "y":
                print("CSV file must have a header. Exiting the program.")
                sys.exit(1)

        convert.convert_files(paths, model, exts)
        dockerfiles = generateImage.generate_dockerfile(paths, model)
    else:
        print(
            "Invalid Arguments. Usage: python script.py same-datamodel [tabular, graph, keyvalue, document]")
        sys.exit(1)
