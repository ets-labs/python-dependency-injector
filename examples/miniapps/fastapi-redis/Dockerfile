FROM python:3.13-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

CMD ["uvicorn", "fastapiredis.application:app", "--host", "0.0.0.0"]
