   FROM postgres:latest

COPY /csvs/ /csvs/
 
ENV POSTGRES_USER=postgres

ENV POSTGRES_PASSWORD=postgres

ENV POSTGRES_DB=postgres

COPY import_data.sh /docker-entrypoint-initdb.d/import_data.sh

RUN chmod +x /docker-entrypoint-initdb.d/import_data.sh

EXPOSE 5432 

VOLUME /var/lib/postgresql/data

CMD ["bash", "-c", "docker-entrypoint.sh postgres"]