# Taskflow API

Enterprise Task and Job Workflow Management REST API built with Python 3.14+, Django 6.1, Django REST Framework, PostgreSQL, Celery, and Redis.

## Features

- **Framework:** Django 6.1 & Django REST Framework
- **Database:** PostgreSQL
- **Documentation:** Automated OpenAPI 3.0 via `drf-spectacular` (Swagger UI & Redoc)
- **Package Management:** Fast dependency resolution using `uv`
- **Environment Management:** Strict separation of config via `python-dotenv`

## API Documentation

Once the development server is running, interactive API documentation is available at:

- **Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **Redoc:** `http://127.0.0.1:8000/api/schema/redoc/`
- **OpenAPI Schema:** `http://127.0.0.1:8000/api/schema/`

## Quick Start

### Prerequisites

- Python 3.14+
- `uv` package manager
- PostgreSQL database server

### Local Setup

1. Clone the repository:
```bash
git clone git@github.com:WhattheAj/Taskflow.git
cd Taskflow
```

2. Install dependencies:
```bash
uv sync
```

3. Environment configuration:
```bash
cp src/.env.example src/.env
```

4. Run database migrations:
```bash
uv run python src/manage.py migrate
```

5. Start the development server:
```bash
uv run python src/manage.py runserver
```

## Upcoming Roadmap

- Custom User Model & Role-Based Access Control (RBAC)
- JWT Authentication (Access & Refresh tokens with Blacklisting)
- Core Job State Machine Workflow Engine
- Asynchronous Task Processing with Celery & Redis
- Automated Testing Suite with `pytest-django`
- Containerization with Docker & Docker Compose
