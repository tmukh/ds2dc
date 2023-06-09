FROM postgres:latest
EXPOSE 5432

COPY /csvs/ /csvs/
 
ENV POSTGRES_USER=postgres

ENV POSTGRES_PASSWORD=postgres

ENV POSTGRES_DB=postgres

COPY import_data.sh /docker-entrypoint-initdb.d/import_data.sh

RUN chmod +x /docker-entrypoint-initdb.d/import_data.sh

EXPOSE 5432 

# Check if the data directory is empty
RUN [ -z "$(ls -A /var/lib/postgresql/data)" ] && touch /firstrun

# Start the PostgreSQL server and execute import_data.sh if it is the first run
CMD if [ -e /firstrun ]; then \
        rm /firstrun && \
        docker-entrypoint.sh postgres && \
        bash -c '/docker-entrypoint-initdb.d/import_data.sh'; \
    else \
        docker-entrypoint.sh postgres; \
    fi