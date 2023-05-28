FROM python:3.11

WORKDIR /
COPY .vscode/settings.json /keyValue files/settings.json
	COPY random/folder/ApacheCalcite-Standardized.json /keyValue files/ApacheCalcite-Standardized.json
	
COPY requirements.txt /files/requirements.txt
RUN pip install --no-cache-dir -r /files/requirements.txt

COPY smartconv/*.py /files/
	CMD [ "python", "/files/convert.py", "same-datamodel", "keyvalue" ]