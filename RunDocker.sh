#!/bin/bash

# Set your PostgreSQL environment variables
PGHOST="localhost"
PGPORT="5432"
PGDATABASE="postgres"
PGUSER="postgres"
PGPASSWORD="postgres"
DOCKERNAME="tabular_container"


docker run --name tabular_container -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=csvs -v pgdata:/var/lib/postgresql/data -d postgrestest 
