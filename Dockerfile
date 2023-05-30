FROM python:3.11

WORKDIR /
COPY data/Chinook.db /csvs/Chinook.db
	COPY data/fake_data.feather /csvs/fake_data.feather
	COPY data/name_data.tsv /csvs/name_data.tsv
	COPY random/subfolder/yellow_tripdata_2023-01.parquet /csvs/yellow_tripdata_2023-01.parquet
	COPY data/fakeadj.adjlist /graphs/fakeadj.adjlist
	COPY data/fakeedgelist.edgelist /graphs/fakeedgelist.edgelist
	COPY data/fakegdf.gdf /graphs/fakegdf.gdf
	COPY data/fakegraphm.graphml /graphs/fakegraphm.graphml
	COPY random/folder/fakegexf.gexf /graphs/fakegexf.gexf
	COPY .vscode/settings.json /keyValue files/settings.json
	COPY random/folder/ApacheCalcite-Standardized.json /keyValue files/ApacheCalcite-Standardized.json
	
COPY requirements.txt /files/requirements.txt
RUN pip install --no-cache-dir -r /files/requirements.txt

COPY smartconv/*.py /files/
	CMD [ "python", "/files/convert.py", "multimodel" ]