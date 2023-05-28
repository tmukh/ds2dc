import scanFilefolder
import generateImage
import sys
import convert
if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print(
            "Invalid Arguments, usage: python convert.py <Data Model> [Extension]")
    elif len(sys.argv) == 2:
        paths=[]
        if sys.argv[1].lower() == "tabular":
            # Handle tabular data model case
            pass
        elif sys.argv[1].lower() == "multimodel":
            # Handle multimodel data model case
            pass
        elif sys.argv[1].lower() == "domain-specific":
            # Handle domain-specific data model case
            pass
        else:
            print("Invalid Data Model, Data model has to be one of the following:\n"
                  "1. multimodel\n"
                  "2. domain-specific\n"
                  "3. same-datamodel [Extension]\n"
                  "4. tabular")
            sys.exit(1)
    elif len(sys.argv) == 3 and sys.argv[1].lower() == "same-datamodel":
        model = sys.argv[2].lower()
        if model == "tabular":
            exts = [".csv", ".xlsx", ".xls", ".tsv",
                   ".parquet", ".feather", ".sqlite", ".db"]
            paths = scanFilefolder.traverseSameDataModel(exts,[],model)
            converted_paths = convert.convert_files(paths,'tabular',exts)
            generateImage.generate_dockerfile(converted_paths,'tabular')

        elif model == "graph":
            exts = [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"]
            paths = scanFilefolder.traverseSameDataModel(exts,[],model)
            converted_paths = convert.convert_files(paths,'graph',exts)
            generateImage.generate_dockerfile(converted_paths,'graph')



        elif model == "keyvalue":
            exts = [".json", ".yaml", ".xml", ".properties"]
            paths = scanFilefolder.traverseSameDataModel(exts,[],model)
            converted_paths = convert.convert_files(paths,'keyvalue',exts)
            generateImage.generate_dockerfile(converted_paths,'keyvalue')



        else:
            print("Invalid Data Model. Available options for same-datamodel are: tabular, graph, keyvalue, nosql")
            sys.exit(1)
    else:
        print("Invalid Arguments. Usage: python script.py same-datamodel [tabular, graph, keyvalue, nosql]")
        sys.exit(1)

    