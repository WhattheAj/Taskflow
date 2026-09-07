# Taskflow API

Enterprise Task and Job Workflow Management REST API built with Python 3.14+, Django 6.1, Django REST Framework, PostgreSQL, Celery, Redis, and Docker.

---

## Technical Highlights

- **Custom User Model & Authentication:** Email-based authentication (`USERNAME_FIELD = 'email'`) with JWT (JSON Web Tokens) and Role-Based Access Control (`ADMIN`, `MANAGER`, `MEMBER`).
- **Workflow State Machine Engine:** Enforced job lifecycle state transitions with strict domain validations and activity logging (`PENDING` -> `IN_PROGRESS` -> `IN_REVIEW` -> `COMPLETED`).
- **High-Performance Database Layer:** PostgreSQL database with compound indexing on query filters (`status`, `priority`, `assignee`) and ORM query optimization (`select_related`, `prefetch_related`) preventing N+1 queries.
- **Caching & Cache Invalidation:** Namespaced Redis caching layer (`django-redis`) with automatic invalidation on mutation events.
- **Asynchronous Background Workers:** Celery worker integration backed by Redis broker for non-blocking notifications.
- **Scheduled Periodic Tasks:** Celery Beat scanner for automated 24-hour job deadline alerts.
- **Automated Testing Suite:** Unit and integration test coverage (`pytest-django` / `TestCase`).
- **OpenAPI 3.0 & Interactive Swagger Docs:** Interactive API specification served via `drf-spectacular`.
- **Multi-Container Docker Architecture:** Fully containerized environment orchestrating Django, PostgreSQL, Redis, Celery Worker, and Celery Beat.

---

## Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.14+ |
| **Web Framework** | Django 6.1 & Django REST Framework 3.18+ |
| **Authentication** | JWT (`djangorestframework-simplejwt`) |
| **Database** | PostgreSQL 16 |
| **Cache & Message Broker** | Redis 7 (`django-redis`) |
| **Task Queue & Scheduler** | Celery 5.6+ & Celery Beat |
| **API Documentation** | OpenAPI 3.0 & Swagger UI (`drf-spectacular`) |
| **Package Manager** | `uv` |
| **Containerization** | Docker & Docker Compose |
| **WSGI Server** | Gunicorn 26.2+ |

---

## API Endpoints Reference

### 1. Authentication & Profile (`/api/users/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/users/register/` | Register a new user account | Public |
| `POST` | `/api/users/token/` | Obtain JWT access & refresh token pair | Public |
| `POST` | `/api/users/token/refresh/` | Refresh JWT access token | Public |
| `GET` | `/api/users/me/` | Retrieve authenticated user profile | Bearer Token |
| `PATCH` | `/api/users/me/` | Update authenticated user profile | Bearer Token |

### 2. Job Categories (`/api/jobs/categories/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/jobs/categories/` | List categories (Cached in Redis) | Bearer Token |
| `POST` | `/api/jobs/categories/` | Create a new category | Bearer Token |
| `GET` | `/api/jobs/categories/{id}/` | Retrieve category detail | Bearer Token |
| `PATCH` | `/api/jobs/categories/{id}/` | Update category | Bearer Token |
| `DELETE` | `/api/jobs/categories/{id}/` | Delete category | Bearer Token |

### 3. Job Management & Workflow (`/api/jobs/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/jobs/` | List jobs (Filterable by status, priority, assignee, category, due date) | Bearer Token |
| `POST` | `/api/jobs/` | Create a new job assignment | Bearer Token |
| `GET` | `/api/jobs/{id}/` | Retrieve job details, comments & activity history | Bearer Token |
| `PATCH` | `/api/jobs/{id}/` | Update job details | Bearer Token |
| `DELETE` | `/api/jobs/{id}/` | Delete job | Bearer Token |
| `PATCH` | `/api/jobs/{id}/status/` | Transition job status via State Machine Engine | Bearer Token |
| `GET` | `/api/jobs/{id}/comments/` | List job discussion comments | Bearer Token |
| `POST` | `/api/jobs/{id}/comments/` | Add a comment to a job | Bearer Token |

### 4. Interactive OpenAPI Documentation (`/api/schema/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/schema/swagger-ui/` | Interactive Swagger UI API documentation | Public |
| `GET` | `/api/schema/redoc/` | Redoc API documentation | Public |
| `GET` | `/api/schema/` | Raw OpenAPI 3.0 Schema | Public |

---

## Job State Machine Lifecycle

State transitions follow a strict domain rulebook managed by `JobStateMachine`:

```text
               +------------+
               |  PENDING   |
               +-----+------+
                  |      \
                  v       \
          +-------+----+   \
          |IN_PROGRESS |    v
          +--+------+--+  +-----------+
            /        \    | CANCELLED |
           /          \   +-----+-----+
          v            v        |
   +------+-----+ +----+---+    |
   | IN_REVIEW  | |COMPLETED|<--+
   +------------+ +--------+
```

- **PENDING:** Initial state on creation. Can transition to `IN_PROGRESS` or `CANCELLED`.
- **IN_PROGRESS:** Active work in progress. Can transition to `IN_REVIEW`, `COMPLETED`, `PENDING`, or `CANCELLED`.
- **IN_REVIEW:** Submitted for verification. Can transition to `COMPLETED`, `IN_PROGRESS` (rework), or `CANCELLED`.
- **COMPLETED:** Finalized state. Can be reopened to `IN_PROGRESS` by managers.
- **CANCELLED:** Cancelled state. Can be reset to `PENDING`.

---

## Quick Start Guide

### Option 1: Running with Docker Compose (Recommended)

Start all services (PostgreSQL, Redis, Django Web, Celery Worker, Celery Beat):

```bash
docker compose up -d
```

Apply database migrations:

```bash
docker compose exec web uv run python src/manage.py migrate
```

Create a superuser for Admin Panel:

```bash
docker compose exec web uv run python src/manage.py createsuperuser
```

Access the interactive API documentation at:
- **Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **Django Admin:** `http://127.0.0.1:8000/admin/`

---

### Option 2: Local Development with `uv`

1. Clone repository and install dependencies:
```bash
git clone git@github.com:WhattheAj/Taskflow.git
cd Taskflow
uv sync
```

2. Environment configuration:
```bash
cp src/.env.example src/.env
```

3. Run migrations and start server:
```bash
uv run python src/manage.py migrate
uv run python src/manage.py runserver
```

---

## Makefile Commands Reference

| Command | Action |
| :--- | :--- |
| `make up` | Launch all containers in background |
| `make down` | Stop and remove all containers |
| `make build` | Rebuild Docker images |
| `make logs` | Stream live container logs |
| `make test` | Run full automated test suite |
| `make migrate` | Execute database migrations |
| `make superuser` | Create Django superuser account |
| `make check` | Run Django system health check |
| `make shell` | Open Django interactive shell inside container |

---

## Automated Test Suite

Run the unit and integration test suite:

```bash
uv run python src/manage.py test jobs
```
