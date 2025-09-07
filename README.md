# Questions API Service

API for Q&A service built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

## Features

- Create, retrieve, and delete questions
- Database migrations with Alembic
- Automated setup with Docker Compose
- Unit tests with pytest

## Tech Stack

- **FastAPI** for backend
- **SQLAlchemy** ORM + **Alembic** migrations
- **PostgreSQL** as database
- **Docker Compose** for deployment
- **pytest** for testing

---

# How to run

## Quickstart

Run this oneliner below

```bash
git clone https://github.com/HossBigft/python-questions-api-service.git \
  && cd python-questions-api-service \
  && pip install uv \
  && uv sync \
  && cp -v env .env \
  && docker compose up -d
```

## Step by step

1.Clone project

```bash
git clone https://github.com/HossBigft/python-questions-api-service.git && cd python-questions-api-service
```

2.Install uv

```bash
pip install uv
```

3.Init project

```bash
uv sync
```

4.Create env file from template

```bash
cp -v env .env
```

5.Start project with docker

```bash
docker compose up -d
```

## Service hosts

API will be available at: http://localhost:8000

Swagger UI: http://localhost:8000/docs
Adminer UI: http://localhost:8080

## To run tests

Run in root dir with active `.venv`

```bash
pytest
```
