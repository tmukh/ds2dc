import os 
file_arr = []
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
    else:
        raise ValueError("Invalid cmd_option. Expected 'graph', 'tabular', or 'keyvalue'.")

    cmd_option = cmd_option.lower()

    if cmd_option == "graph":
        cmd = 'CMD [ "python", "/files/convert.py", "same-datamodel", "graph" ]'
    elif cmd_option == "tabular":
        cmd = 'CMD [ "python", "/files/convert.py", "same-datamodel" , "tabular"]'
    elif cmd_option == "keyvalue":
        cmd = 'CMD [ "python", "/files/convert.py", "same-datamodel", "keyvalue" ]'
    else:
        raise ValueError("Invalid cmd_option. Expected 'graph', 'same-datamodel', or 'keyvalue'.")

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
