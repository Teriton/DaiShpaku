FROM python:3.12.7-slim

WORKDIR /usr/src/app

COPY ./main.py ./design.py ./databaseManager.py ./requirements.txt ./Dockerfile ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./main.py"]