FROM python:3.9-slim

WORKDIR /app

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update \
    && apt-get -y install postgresql

RUN apt-get update \
    && pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


EXPOSE 8000