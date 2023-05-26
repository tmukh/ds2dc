def generate_dockerfile(files):
    # Create the Dockerfile content
    dockerfile_content = f'''\
    FROM python:3.11

    WORKDIR /
    '''

    docker_files=""
    for x in files:
        docker_files += (f"COPY {x} /{x}") + "\n\t"

   

    rest = '''
    COPY convert.py /files/convert.py
    COPY requirements.txt /files/requirements.txt
    RUN pip install --no-cache-dir -r /files/requirements.txt


    CMD [ "python", "/files/convert.py" ]
    '''
    finalstr = dockerfile_content + docker_files + rest
    print(finalstr)
    # Write the content to a Dockerfile
    with open('Dockerfile', 'w') as dockerfile:
        dockerfile.write(finalstr)

