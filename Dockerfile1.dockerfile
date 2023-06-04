FROM postgres:latest
EXPOSE 5432

COPY /csvs/ /csvs/
COPY populate_csvs.sh .