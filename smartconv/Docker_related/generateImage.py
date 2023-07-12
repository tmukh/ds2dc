def generate_docker_compose(file_paths, data_model):
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
        tabular_extensions = [".csv", ".xlsx", ".xls", ".tsv",
                              ".parquet", ".feather", ".sqlite", ".db"]
        graph_extensions = [".graphml", ".gml", ".gexf",
                            ".gdf", ".edgelist", ".adjlist"]
        keyvalue_extensions = [".json", ".yaml", ".xml", ".properties"]
        document_extensions = [".json", ".bson", ".yaml", ".csv"]

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
    docker_compose_body = "  postgres:\n"
    docker_compose_body += "    image: postgres:latest\n"
    docker_compose_body += "    environment:\n"
    docker_compose_body += "      POSTGRES_USER: postgres\n"
    docker_compose_body += "      POSTGRES_PASSWORD: postgres\n"
    docker_compose_body += "      POSTGRES_DB: postgres\n"
    docker_compose_body += "    volumes:\n"
    docker_compose_body += "      - ./csvs:/csvs\n"
    docker_compose_body += "      - ./import_scripts/import_tabular_data.sh:/docker-entrypoint-initdb.d/import_tabular_data.sh\n"
    docker_compose_body += "      - ./data:/var/lib/postgresql/data\n\n"
    docker_compose_body += "    ports:\n"
    docker_compose_body += "      - 5432:5432\n"

    return docker_compose_body


def generate_graph_docker_compose(file_paths):
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
    docker_compose_body += "      - ./graphs:/var/lib/neo4j/import\n"
    docker_compose_body += "      - ./import_scripts/import_graph_data.sh:/var/lib/neo4j/import/import_graph_data.sh\n"
    docker_compose_body += "    ports:\n"
    docker_compose_body += "      - 7474:7474\n"
    docker_compose_body += "      - 7687:7687\n\n"

    return docker_compose_body


def generate_keyvalue_docker_compose(file_paths):
    docker_compose_body = "  redis:\n"
    docker_compose_body += "    image: redis:latest\n"
    docker_compose_body += "    volumes:\n"
    docker_compose_body += "      - ./kv_files:/kv_files\n"
    docker_compose_body += "      - ./kv_to_redis.py:/kv_to_redis.py\n"
    docker_compose_body += "    command: sh -c \"redis-server & sleep 5 && python3 /kv_to_redis.py && tail -f /dev/null\"\n"
    docker_compose_body += "    ports:\n"
    docker_compose_body += "      - 6379:6379\n\n"

    return docker_compose_body


def generate_document_docker_compose(file_paths):
    docker_compose_body = "  mongo:\n"
    docker_compose_body += "    image: mongo:latest\n"
    docker_compose_body += "    environment:\n"
    docker_compose_body += "      MONGO_INITDB_DATABASE: import_db\n"
    docker_compose_body += "      MONGO_INITDB_ROOT_USERNAME: admin\n"
    docker_compose_body += "      MONGO_INITDB_ROOT_PASSWORD: 123\n"
    docker_compose_body += "    volumes:\n"
    docker_compose_body += "      - ./doc_files:/docker-entrypoint-initdb.d\n"
    docker_compose_body += "      - ./smartconv/import_scripts/import_docs.sh:/docker-entrypoint-initdb.d/import.sh\n"
    docker_compose_body += "    command: mongod --bind_ip_all\n"
    docker_compose_body += "    ports:\n"
    docker_compose_body += "      - 27017:27017\n\n"

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
