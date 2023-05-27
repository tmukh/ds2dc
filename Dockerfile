    FROM python:3.11

    WORKDIR /
    COPY .vscode/settings.json /.vscode/settings.json
	COPY data/ApacheCalcite-Standardized.json /data/ApacheCalcite-Standardized.json
	
    COPY convert.py /files/convert.py
    COPY requirements.txt /files/requirements.txt
    RUN pip install --no-cache-dir -r /files/requirements.txt


    CMD [ "python", "/files/convert.py" ]
    