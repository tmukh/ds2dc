    FROM python:3.11

    WORKDIR /
    COPY data/Chinook.db /data/Chinook.db
	COPY data/fake_data.feather /data/fake_data.feather
	COPY data/name_data.tsv /data/name_data.tsv
	COPY data/title_aka_data.tsv /data/title_aka_data.tsv
	COPY data/title_basic_data.tsv /data/title_basic_data.tsv
	COPY data/yellow_tripdata_2023-01.parquet /data/yellow_tripdata_2023-01.parquet
	
    COPY convert.py /files/convert.py
    COPY requirements.txt /files/requirements.txt
    RUN pip install --no-cache-dir -r /files/requirements.txt


    CMD [ "python", "/files/convert.py" ]
    