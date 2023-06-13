import os


def get_extension(file_path):
    # Extract the extension from the file path
    parts = file_path.split('.')
    if len(parts) > 1:
        return '.' + parts[-1]
    else:
        return ''

def write_dockerfiles(dockerfiles):
    for i, dockerfile in enumerate(dockerfiles):
        with open(f"Dockerfile{i+1}.dockerfile", "w") as file:
            file.write(dockerfile)
        print(f"Dockerfile{i+1} generated successfully.")
        
def generate_dockerfile(files, cmd_option):
    exts_tabular = [".csv", ".xlsx", ".xls", ".tsv", ".parquet", ".feather", ".sqlite", ".db"]
    exts_graph = [".graphml", ".gml", ".gexf", ".gdf", ".edgelist", ".adjlist"]
    exts_keyvalue = [".json", ".yaml", ".xml", ".properties"]

    dockerfiles = []
    
    def graph_tool(cmd_option):
        # Add setup for graph tools, like Neo4j server
        return f"FROM neo4j:latest\n\n"
    
    def tabular_tool(cmd_option):
        # Add setup for tabular tools, like PostgreSQL server
        return f"FROM postgres:latest\n\n"
    
    def keyvalue_tool(cmd_option):
        # Add setup for key-value tools, like Redis server
        return f"RUN setup_redis\n\n"
    
    def multimodel_tool(cmd_option):
        # Add setup for multimodel tools, if needed
        return ""
    
    def get_dockerfile_header(cmd_option):
        # Get the appropriate tool setup based on cmd_option
        if cmd_option == "graph":
            return graph_tool(cmd_option)
        elif cmd_option == "tabular":
            return tabular_tool(cmd_option)
        elif cmd_option == "keyvalue":
            return keyvalue_tool(cmd_option)
        elif cmd_option == "multimodel":
            return multimodel_tool(cmd_option)
        else:
            raise ValueError("Invalid cmd_option. Expected 'graph', 'tabular', 'keyvalue', or 'multimodel'.")
    def create_docker_file_based_on_cmd(cmd_option):
        if cmd_option == "graph":
            graph_dir = "/graphs/"
            dockerfile = f"""{dockerfile_header}COPY {graph_dir} {graph_dir}\n
ENV NEO4J_PLUGINS='["apoc"]'
ENV NEO4J_AUTH=neo4j/password
ENV NEO4J_dbms_security_procedures_unrestricted=apoc.*
ENV NEO4J_apoc_export_file_enabled=true
ENV NEO4J_apoc_import_file_enabled=true
ENV NEO4J_apoc_import_file_use_neo4j_config=true

COPY /graphs/ /var/lib/neo4j/import/
RUN echo 'dbms.security.allow_csv_import_from_file_urls=true' >> /var/lib/neo4j/conf/neo4j.conf
RUN chown -R neo4j:neo4j /var/lib/neo4j/import/
RUN chmod -R 644 /var/lib/neo4j/import/

# Copy the import script
COPY /import_scripts/import_graph_data.sh /var/lib/neo4j/import/import_graph_data.sh
RUN chmod +x /var/lib/neo4j/import/import_graph_data.sh

EXPOSE 7474 7687 7473

CMD ["neo4j"]"""
            dockerfiles.append(dockerfile)
        
        elif cmd_option == "tabular":
            csv_dir = "/csvs/"
            dockerfile = f"""   {dockerfile_header}COPY {csv_dir} {csv_dir}\n 
ENV POSTGRES_USER=postgres\n
ENV POSTGRES_PASSWORD=postgres\n
ENV POSTGRES_DB=postgres\n
COPY /import_scripts/import_tabular_data.sh /docker-entrypoint-initdb.d/import_tabular_data.sh\n
RUN chmod +x /docker-entrypoint-initdb.d/import_tabular_data.sh\n
EXPOSE 5432 \n
VOLUME /var/lib/postgresql/data\n
CMD ["bash", "-c", "docker-entrypoint.sh postgres"]"""
            dockerfiles.append(dockerfile)
        
        elif cmd_option == "keyvalue":
            kv_dir = "/keyValue files/"
            dockerfile = f"""{dockerfile_header}COPY {kv_dir} {kv_dir}\n
FROM redis
EXPOSE 6379
COPY /kv_files/ /kv_files/
COPY /kv_to_redis.py /kv_to_redis.py
RUN chmod +x /kv_to_redis.py
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install redis
# Set the entrypoint to start the Redis server
ENTRYPOINT ["sh", "-c", "redis-server & sleep 5 && python3 /kv_to_redis.py && tail -f /dev/null"]"""
            dockerfiles.append(dockerfile)
   
    
    
    
    
    
    dockerfile_header = get_dockerfile_header(cmd_option)
    
    if cmd_option == "multimodel":
        graph_files = [path for path in files if get_extension(path).lower() in exts_graph]
        csv_files = [path for path in files if get_extension(path).lower() in exts_tabular]
        kv_files = [path for path in files if get_extension(path).lower() in exts_keyvalue]

        if graph_files:
            dockerfile_header = get_dockerfile_header("graph")
            create_docker_file_based_on_cmd("graph")

        if csv_files:
            dockerfile_header = get_dockerfile_header("tabular")
            create_docker_file_based_on_cmd("tabular")
        if kv_files:
            dockerfile_header = get_dockerfile_header("keyvalue")
            create_docker_file_based_on_cmd("keyvalue")
    elif cmd_option in ['tabular','graph','keyvalue']:
        get_dockerfile_header(cmd_option)
        create_docker_file_based_on_cmd(cmd_option)
    else:
        raise ValueError("Invalid cmd_option. Expected 'graph', 'tabular', 'keyvalue', or 'multimodel'.")
    
    return dockerfiles

