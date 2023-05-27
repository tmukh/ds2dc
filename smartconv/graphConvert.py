import os
import networkx as nx

def convert_to_graphml(input_file):
    # Create the output directory if it doesn't exist
    output_dir = "graph files"
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file path
    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}.graphml")

    # Determine the file extension
    file_extension = input_file.split(".")[-1]

    # Load the graph from the input file based on its extension
    if file_extension == "edgelist":
        graph = nx.read_edgelist(input_file)
    elif file_extension == "adjlist":
        graph = nx.read_adjlist(input_file)
    elif file_extension == "gexf":
        graph = nx.read_gexf(input_file)
    elif file_extension == "gml":
        graph = nx.read_gml(input_file)
    elif file_extension == "graphml":
        graph = nx.read_graphml(input_file)
    else:
        print("Unsupported file extension.")
        return

    # Write the graph to the output file in GraphML format
    nx.write_graphml(graph, output_file)
    print(f"Conversion successful. Graph saved to: {output_file}")