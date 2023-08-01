import run_converter
import os
tabular_extensions = [".csv", ".xlsx", ".xls", ".tsv",
                        ".parquet", ".feather", ".sqlite", ".db"]
graph_extensions = [".graphml", ".gml", ".gexf",
                    ".gdf", ".edgelist", ".adjlist"]
keyvalue_extensions = [".json", ".yaml", ".xml", ".properties"]
document_extensions = [".json", ".bson", ".yaml", ".csv"]
def generate_docker_compose(file_paths, data_model, optionalArcPath):
    docker_compose = "version: '3'\n\n"
    docker_compose += "services:\n"

    if data_model == "tabular":
        docker_compose += generate_tabular_docker_compose(file_paths)

    elif data_model == "graph":
        docker_compose += generate_graph_docker_compose(file_paths)

    elif data_model == "keyvalue":
        docker_compose += generate_keyvalue_docker_compose(file_paths)

    elif data_model == "document":
        docker_compose += generate_document_docker_compose(file_paths)

    elif data_model == "multimodel":


        services = []

        if any(file_path.endswith(tuple(tabular_extensions)) for file_path in file_paths):
            services.append(generate_tabular_docker_compose(file_paths))

        if any(file_path.endswith(tuple(graph_extensions)) for file_path in file_paths):
            services.append(generate_graph_docker_compose(file_paths))

        if any(file_path.endswith(tuple(keyvalue_extensions)) for file_path in file_paths):
            services.append(generate_keyvalue_docker_compose(file_paths))

        if any(file_path.endswith(tuple(document_extensions)) for file_path in file_paths):
            services.append(generate_document_docker_compose(file_paths))

        docker_compose += "\n".join(services)
    elif data_model == 'domain-specific':
        services = []
        services.append(generate_domain_specific_docker_compose(optionalArcPath))
        if any(file_path.endswith(tuple(tabular_extensions)) for file_path in file_paths):
            services.append(generate_tabular_docker_compose(file_paths))

        if any(file_path.endswith(tuple(graph_extensions)) for file_path in file_paths):
            services.append(generate_graph_docker_compose(file_paths))

        if any(file_path.endswith(tuple(keyvalue_extensions)) for file_path in file_paths):
            services.append(generate_keyvalue_docker_compose(file_paths))

        if any(file_path.endswith(tuple(document_extensions)) for file_path in file_paths):
            services.append(generate_document_docker_compose(file_paths))
        docker_compose += "\n".join(services)

    else:
        raise ValueError("Invalid data model type")

    docker_compose += generate_drill_docker_compose()
    docker_compose += "\nnetworks:\n"
    docker_compose += "  default:\n"
    docker_compose += "    name: ds2dc_network\n"
    docker_compose += "    driver: bridge\n"
    docker_compose += "    driver_opts:\n"
    docker_compose += "      encrypted: ''\n"

    write_docker_compose(docker_compose, "docker-compose.yml")

    
def write_docker_compose(docker_compose_content, filename):
    with open(filename, "w") as f:
        f.write(docker_compose_content)


def generate_tabular_docker_compose(file_paths):
    script_dir = run_converter.script_dir
    import_script = os.path.join(script_dir, "import_scripts", "import_tabular_data.sh")  # Adjust "import_tabular_data.sh" with the actual filename
    data_volume = os.path.join(script_dir, "data")  # Adjust "data" with the actual path relative to script_dir

    docker_compose_body = f"  postgres:\n"
    docker_compose_body += f"    image: postgres:latest\n"
    docker_compose_body += f"    environment:\n"
    docker_compose_body += f"      POSTGRES_USER: postgres\n"
    docker_compose_body += f"      POSTGRES_PASSWORD: postgres\n"
    docker_compose_body += f"      POSTGRES_DB: postgres\n"
    docker_compose_body += f"    volumes:\n"
    docker_compose_body += f"      - ./csvs/:/csvs\n"
    docker_compose_body += f"      - {import_script}:/docker-entrypoint-initdb.d/import_tabular_data.sh\n"
    docker_compose_body += f"      - {data_volume}:/var/lib/postgresql/data\n\n"
    docker_compose_body += f"    ports:\n"
    docker_compose_body += f"      - 5432:5432\n"

    return docker_compose_body


def generate_graph_docker_compose(file_paths):
    script_dir = run_converter.script_dir
    csvs_volume = os.path.join(script_dir, "graphs")  # Adjust "csvs" with the actual path relative to script_dir
    import_script = os.path.join(script_dir, "import_scripts", "import_graph_data.sh")  # Adjust "import_tabular_data.sh" with the actual filename
    docker_compose_body = "  neo4j:\n"
    docker_compose_body += "    image: neo4j:latest\n"
    docker_compose_body += "    environment:\n"
    docker_compose_body += "      NEO4J_PLUGINS: 'apoc'\n"
    docker_compose_body += "      NEO4J_AUTH: neo4j/password\n"
    docker_compose_body += "      NEO4J_dbms_security_procedures_unrestricted: apoc.*\n"
    docker_compose_body += "      NEO4J_apoc_export_file_enabled: 'true'\n"
    docker_compose_body += "      NEO4J_apoc_import_file_enabled: 'true'\n"
    docker_compose_body += "      NEO4J_apoc_import_file_use_neo4j_config: 'true'\n"
    docker_compose_body += "    volumes:\n"
    docker_compose_body += "      - ./graphs/:/var/lib/neo4j/import\n"
    docker_compose_body += f"      - {import_script}:/var/lib/neo4j/import/import_graph_data.sh\n"
    docker_compose_body += "    ports:\n"
    docker_compose_body += "      - 7474:7474\n"
    docker_compose_body += "      - 7687:7687\n\n"

    return docker_compose_body


def generate_keyvalue_docker_compose(file_paths):
    script_dir = run_converter.script_dir
    init_script = os.path.join(script_dir, "init_scripts", "init_redis.sh")  # Adjust "import_tabular_data.sh" with the actual filename
    import_script = os.path.join(script_dir, "import_scripts", "import_kv_data.sh")  # Adjust "import_tabular_data.sh" with the actual filename
    docker_compose_body = "  redis:\n"
    docker_compose_body += "    image: redis:latest\n"
    docker_compose_body += "    volumes:\n"
    docker_compose_body += "     - ./kv_files/:/kv_files\n"
    docker_compose_body += f"     - {import_script}:/docker-entrypoint-initdb.d/import.sh \n"
    docker_compose_body += f"     - {init_script}:/init_redis.sh \n"
    docker_compose_body += "    command: /init_redis.sh \n"
    docker_compose_body += "    ports:\n"
    docker_compose_body += "      - 6379:6379\n\n"

    return docker_compose_body


def generate_document_docker_compose(file_paths):
    script_dir = run_converter.script_dir
    init_script = os.path.join(script_dir, "init_scripts", "init_mongo.sh")
    import_script = os.path.join(script_dir, "import_scripts", "import_docs.sh")  # Adjust "import_docs.sh" with the actual filename

    docker_compose_body = f"  mongo:\n"
    docker_compose_body += f"    image: mongo:latest\n"
    docker_compose_body += f"    environment:\n"
    docker_compose_body += f"      MONGO_INITDB_DATABASE: import_db\n"
    docker_compose_body += f"      MONGO_INITDB_ROOT_USERNAME: admin\n"
    docker_compose_body += f"      MONGO_INITDB_ROOT_PASSWORD: 123\n"
    docker_compose_body += f"    volumes:\n"
    docker_compose_body += f"      - ./doc_files/:/docker-entrypoint-initdb.d\n"
    docker_compose_body += f"      - {import_script}:/docker-entrypoint-initdb.d/import.sh\n"
    docker_compose_body += f"      - {init_script}:/init_mongo.sh\n"
    docker_compose_body += f"    command: /init_mongo.sh \n"
    docker_compose_body += f"    ports:\n"
    docker_compose_body += f"      - 27017:27017\n\n"

    return docker_compose_body

def generate_drill_docker_compose():
    drill_docker_compose = "  drill:\n"
    drill_docker_compose += "    image: apache/drill:latest\n"
    drill_docker_compose += "    ports:\n"
    drill_docker_compose += "      - '8047:8047'\n"
    drill_docker_compose += "    stdin_open: true\n"
    # drill_docker_compose += "    depends_on:\n"
    # drill_docker_compose += "      - postgres\n"
    # drill_docker_compose += "      - mongo\n\n"

    return drill_docker_compose


def generate_domain_specific_docker_compose(optionalArcPath):
    script_dir = run_converter.script_dir
    init_script = os.path.join(script_dir, "init_scripts", "init_arc.sh")  # Adjust "import_docs.sh" with the actual filename

    
    docker_compose = f"  arccommander_container:\n"
    docker_compose += f"    image: ubuntu:latest\n"
    docker_compose += f"    container_name: arccommander_container\n"
    docker_compose += f"    command:  /arc_files/init_arc.sh \n"
    # bash -c  \"apt update && \n"
    # docker_compose += f"             apt install -y wget libicu-dev git && \n"
    # docker_compose += f"             wget https://github.com/nfdi4plants/arcCommander/releases/download/v0.4.0-linux.x64/arc && \n"
    # docker_compose += f"             chmod u+x arc && \n"
    # docker_compose += f"             if ! [ -d \"$HOME/bin\" ]; then mkdir \"$HOME/bin\"; fi && \n"
    # docker_compose += f"             mv arc $HOME/bin/ && \n"
    # docker_compose += f"             source ~/.bashrc && \n"
    # docker_compose += f"             arc --version && \n"
    # docker_compose += f"             apt install -y git-lfs && \n"
    # docker_compose += f"             git lfs install &&\n"
    # docker_compose += f"             cd arc_files && \n"
    # docker_compose += f"             arc export > metadata.json && \n"
    # docker_compose += f"             tail -f /dev/null \"\n"
    docker_compose += f"    volumes:\n"
    docker_compose += f"      - ./:/arc_files\n"
    docker_compose += f"      -  {init_script}:/arc_files/init_arc.sh"

    return docker_compose