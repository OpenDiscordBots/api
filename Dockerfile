FROM python:3.10-slim-buster

WORKDIR /app

RUN apt update && apt install -y gcc

RUN pip install poetry

COPY pyproject.toml /app
COPY poetry.lock /app

RUN poetry install

COPY . /app

CMD ["sh", "entrypoint.sh"]
