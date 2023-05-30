import os

file_arr = []
exts_tabular = [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"]
exts_graph = [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"]
exts_keyvalue = [".json", ".yaml", ".xml", ".properties"]
def get_extension(file_path):
    # Extract the extension from the file path
    parts = file_path.split('.')
    if len(parts) > 1:
        return '.' + parts[-1]
    else:
        return ''

def generate_dockerfile(files, cmd_option):
    # Create the Dockerfile content
    dockerfile_content = '''\
FROM python:3.11

WORKDIR /
'''

    docker_files = ""

    if cmd_option == "graph":
        graph_dir = "/graphs/"
        for path in files:
            filename = os.path.basename(path)
            docker_files += f"COPY {path} {graph_dir}{filename}\n\t"
    elif cmd_option == "tabular":
        csv_dir = "/csvs/"
        for path in files:
            filename = os.path.basename(path)
            docker_files += f"COPY {path} {csv_dir}{filename}\n\t"
    elif cmd_option == "keyvalue":
        kv_dir = "/keyValue files/"
        for path in files:
            filename = os.path.basename(path)
            docker_files += f"COPY {path} {kv_dir}{filename}\n\t"
    elif cmd_option == "multimodel":
        for path in files:
            extension = get_extension(path)
            if extension.lower() in exts_graph:
                graph_dir = "/graphs/"
                filename = os.path.basename(path)
                docker_files += f"COPY {path} {graph_dir}{filename}\n\t"
            elif extension.lower() in exts_tabular:
                csv_dir = "/csvs/"
                filename = os.path.basename(path)
                docker_files += f"COPY {path} {csv_dir}{filename}\n\t"
            elif extension.lower() in exts_keyvalue:
                kv_dir = "/keyValue files/"
                filename = os.path.basename(path)
                docker_files += f"COPY {path} {kv_dir}{filename}\n\t"
            else:
                print(f"Unsupported file extension: {extension}")
    else:
        raise ValueError("Invalid cmd_option. Expected 'graph', 'tabular', 'keyvalue', or 'multimodel'.")

    cmd_option = cmd_option.lower()

    if cmd_option == "graph":
        cmd = 'CMD [ "python", "/files/convert.py", "same-datamodel", "graph" ]'
    elif cmd_option == "tabular":
        cmd = 'CMD [ "python", "/files/convert.py", "same-datamodel" , "tabular"]'
    elif cmd_option == "keyvalue":
        cmd = 'CMD [ "python", "/files/convert.py", "same-datamodel", "keyvalue" ]'
    elif cmd_option == "multimodel":
        cmd = 'CMD [ "python", "/files/convert.py", "multimodel" ]'
    else:
        raise ValueError("Invalid cmd_option. Expected 'graph', 'tabular', 'keyvalue', or 'multimodel'.")

    rest = '''
COPY requirements.txt /files/requirements.txt
RUN pip install --no-cache-dir -r /files/requirements.txt

'''

    finalstr = dockerfile_content + docker_files + rest
    finalstr += 'COPY smartconv/*.py /files/\n\t'
    finalstr += cmd

    # Write the content to a Dockerfile
    with open('Dockerfile', 'w') as dockerfile:
        dockerfile.write(finalstr)
