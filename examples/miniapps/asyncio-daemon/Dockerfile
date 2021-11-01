FROM python:3.10-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY . /code/

RUN apt-get install openssl \
 && pip install --upgrade pip \
 && pip install -r requirements.txt \
 && rm -rf ~/.cache

CMD ["python", "-m", "monitoringdaemon"]
