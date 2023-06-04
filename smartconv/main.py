import scanFilefolder
import generateImage
import sys
import convert
if __name__ == "__main__":
        if len(sys.argv) == 1 or len(sys.argv) > 3:
            print(
                "Invalid Arguments, usage: python convert.py <Data Model> [Extension]")
        elif len(sys.argv) == 2:
            if sys.argv[1].lower() == "multimodel":
                exts_tabular = [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"]
                exts_graph = [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"]
                exts_keyvalue = [".json", ".yaml", ".xml", ".properties"]
                
                tabular_paths = scanFilefolder.traverseMultiDataModels(exts_tabular)[0]
                graph_paths = scanFilefolder.traverseMultiDataModels(exts_graph)[1]
                keyvalue_paths = scanFilefolder.traverseMultiDataModels(exts_keyvalue)[2]
                all_paths  = [item for sublist in [tabular_paths, graph_paths, keyvalue_paths] for item in sublist]
                if len(all_paths) > 0:
                    # Process all paths together
                    converted_paths = convert.convert_files_by_extension(all_paths)
                    dockerfiles = generateImage.generate_dockerfile(converted_paths, "multimodel")
                    generateImage.write_dockerfiles(dockerfiles)
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
                exts = [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"]
            elif model == "graph":
                exts = [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"]
            elif model == "keyvalue":
                exts = [".json", ".yaml", ".xml", ".properties"]
            else:
                print("Invalid Data Model. Available options for same-datamodel are: tabular, graph, keyvalue")
                sys.exit(1)
            paths = scanFilefolder.traverseSameDataModel(exts)
            convert.convert_files(paths, model, exts)
            dockerfiles = generateImage.generate_dockerfile(paths, model)
            generateImage.write_dockerfiles(dockerfiles)

        else:
            print(
                "Invalid Arguments. Usage: python script.py same-datamodel [tabular, graph, keyvalue]")
            sys.exit(1)
        