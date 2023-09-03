import os


def generate_dockerfile(file_paths, data_model):
    dockerfile = ""

    if data_model == "tabular":
        dockerfile += generate_tabular_dockerfile(file_paths)
        write_dockerfile(dockerfile, "tabular.dockerfile")

    elif data_model == "graph":
        dockerfile += generate_graph_dockerfile(file_paths)
        write_dockerfile(dockerfile, "graph.dockerfile")
    elif data_model == "keyvalue":
        dockerfile += generate_keyvalue_dockerfile(file_paths)
        write_dockerfile(dockerfile, "keyvalue.dockerfile")


    elif data_model == "document":
        dockerfile += generate_document_dockerfile(file_paths)
        write_dockerfile(dockerfile, "document.dockerfile")

    elif data_model == "multimodel":

        tabular_extensions = [".csv", ".xlsx", ".xls", ".tsv",
                              ".parquet", ".feather", ".sqlite", ".db"]
        graph_extensions = [".graphml", ".gml", ".gexf",
                            ".gdf", ".edgelist", ".adjlist"]
        keyvalue_extensions = [".json", ".yaml"],# ".xml", ".properties"]
        document_extensions = [".json", ".bson", ".yaml", ".csv"]

        tabular_files = [file_path for file_path in file_paths if any(
            file_path.endswith(extension) for extension in tabular_extensions)]
        graph_files = [file_path for file_path in file_paths if any(
            file_path.endswith(extension) for extension in graph_extensions)]
        keyvalue_files = [file_path for file_path in file_paths if any(
            file_path.endswith(extension) for extension in keyvalue_extensions)]
        document_files = [file_path for file_path in file_paths if any(
            file_path.endswith(extension) for extension in document_extensions)]

        if tabular_files:
            dockerfile = generate_tabular_dockerfile(tabular_files)
            write_dockerfile(dockerfile, "tabular.dockerfile")

        if graph_files:
            dockerfile = generate_graph_dockerfile(graph_files)
            write_dockerfile(dockerfile, "graph.dockerfile")

        if keyvalue_files:
            dockerfile = generate_keyvalue_dockerfile(keyvalue_files)
            write_dockerfile(dockerfile, "keyvalue.dockerfile")

        if document_files:
            dockerfile = generate_document_dockerfile(document_files)
            write_dockerfile(dockerfile, "document.dockerfile")

    else:
        raise ValueError("Invalid data model type")

def write_dockerfile(dockerfile_content, filename):
    with open(filename, "w") as f:
        f.write(dockerfile_content)

def generate_tabular_dockerfile(file_paths):
    dockerfile_body = "FROM postgres:latest\n\n"
    dockerfile_body += "ENV POSTGRES_USER=postgres\n"
    dockerfile_body += "ENV POSTGRES_PASSWORD=postgres\n"
    dockerfile_body += "ENV POSTGRES_DB=postgres\n"
    dockerfile_body += "COPY csvs/ /csvs/ \n"
    dockerfile_body += "COPY /import_scripts/import_tabular_data.sh /docker-entrypoint-initdb.d/import_tabular_data.sh\n"
    dockerfile_body += "RUN chmod +x /docker-entrypoint-initdb.d/import_tabular_data.sh \n"
    dockerfile_body += "EXPOSE 5432\n"
    dockerfile_body += "VOLUME /var/lib/postgresql/data\n"
    dockerfile_body += 'CMD ["bash", "-c", "docker-entrypoint.sh postgres"]\n'

    return dockerfile_body


def generate_graph_dockerfile(file_paths):
    dockerfile_body = "FROM neo4j:latest\n\n"
    dockerfile_body += 'ENV NEO4J_PLUGINS=\'["apoc"]\'\n'
    dockerfile_body += "ENV NEO4J_AUTH=neo4j/password\n"
    dockerfile_body += "ENV NEO4J_dbms_security_procedures_unrestricted=apoc.*\n"
    dockerfile_body += "ENV NEO4J_apoc_export_file_enabled=true\n"
    dockerfile_body += "ENV NEO4J_apoc_import_file_enabled=true\n"
    dockerfile_body += "ENV NEO4J_apoc_import_file_use_neo4j_config=true\n\n"
    dockerfile_body += "COPY graphs/ /var/lib/neo4j/import/\n"
    dockerfile_body += "RUN echo 'dbms.security.allow_csv_import_from_file_urls=true' >> /var/lib/neo4j/conf/neo4j.conf\n"
    dockerfile_body += "RUN chown -R neo4j:neo4j /var/lib/neo4j/import/\n"
    dockerfile_body += "RUN chmod -R 644 /var/lib/neo4j/import/\n\n"
    dockerfile_body += "COPY /import_scripts/import_graph_data.sh /var/lib/neo4j/import/import_graph_data.sh\n"
    dockerfile_body += "RUN chmod +x /var/lib/neo4j/import/import_graph_data.sh\n\n"
    dockerfile_body += "EXPOSE 7474 7687 7473\n"
    dockerfile_body += 'CMD ["neo4j"]\n'

    return dockerfile_body


def generate_keyvalue_dockerfile(file_paths):
    dockerfile_body = "FROM redis:latest\n\n"
    dockerfile_body += "EXPOSE 6379\n"
    dockerfile_body += "COPY kv_files/ /kv_files/\n"
    dockerfile_body += "COPY /kv_to_redis.py /kv_to_redis.py\n"
    dockerfile_body += "RUN chmod +x /kv_to_redis.py\n"
    dockerfile_body += "RUN apt-get update && apt-get install -y python3 python3-pip\n"
    dockerfile_body += "RUN pip3 install redis\n"
    dockerfile_body += 'ENTRYPOINT ["sh", "-c", "redis-server & sleep 5 && python3 /kv_to_redis.py && tail -f /dev/null"]\n'

    return dockerfile_body


def generate_document_dockerfile(file_paths):
    dockerfile_body = "FROM mongo:latest\n\n"
    dockerfile_body += "ENV MONGO_INITDB_DATABASE=import_db\n"
    dockerfile_body += "ENV MONGO_INITDB_ROOT_USERNAME=admin\n"
    dockerfile_body += "ENV MONGO_INITDB_ROOT_PASSWORD=123\n"
    dockerfile_body += "COPY doc_files/ /docker-entrypoint-initdb.d/\n"
    dockerfile_body += "COPY smartconv/import_scripts/import_docs.sh /docker-entrypoint-initdb.d/import.sh \n"
    dockerfile_body += 'CMD ["mongod", "--bind_ip_all"]\n'
    
def generate_drill_docker_compose():
    drill_docker_compose = "  drill:\n"
    drill_docker_compose += "    image: apache/drill:latest\n"
    drill_docker_compose += "    ports:\n"
    drill_docker_compose += "      - '8047:8047'\n"
    drill_docker_compose += "    stdin_open: true\n"
    drill_docker_compose += "    depends_on:\n"
    drill_docker_compose += "      - postgres\n"
    drill_docker_compose += "      - mongo\n\n"

    return dockerfile_body
