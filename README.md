## 📊 Live Links

<p align="center">

<a href="https://hyper-scale-ops-dev-218cc42920d8.herokuapp.com/">
    <img src="https://img.shields.io/badge/🚀-Live%20Application-430098?style=for-the-badge" />
</a>

<a href="https://p.us5.datadoghq.com/sb/8e9bd3b1-7001-11f1-aae3-c2753782a27a-994485ddc16ff7de20d382368a9bf932">
    <img src="https://img.shields.io/badge/📈-Datadog%20Dashboard-632CA6?style=for-the-badge&logo=datadog&logoColor=white" />
</a>

</p>

<p align="center">
<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&height=4&color=0:334155,100:475569"/>
</p>

# Hyper Scale Ops

Hyper Scale Ops is a modern full-stack web application (I used jinja2 templates for frontend) designed to demonstrate strong backend engineering, clean API design, and practical product thinking. The project showcases a student management system that combines a FastAPI-powered backend, database-driven business logic, and a simple user-facing interface suitable for internal tools or lightweight operational workflows.

This README is written with a recruiter and technical manager audience in mind, highlighting not just what the project does, but how it is built, how it scales in structure, and how it reflects professional software development practices.

## Why This Project Matters

This project demonstrates:

- End-to-end application development using a modern Python stack
- Clean separation between API, service, schema, and data layers
- Production-minded design choices such as async database access and migration management
- Test-driven validation of critical CRUD workflows
- A practical, business-friendly use case that is easy to understand and demonstrate

## Core Capabilities

The application supports:

- Creating, reading, updating, and deleting student records
- Managing related student profile details such as address and guardian information
- Serving both a web interface and a REST API
- Performing health and database connectivity checks
- Maintaining data integrity through structured models and migrations

## Technology Stack

- Backend: FastAPI
- Async ORM: SQLAlchemy
- Database: PostgreSQL
- Migrations: Alembic
- Templating: Jinja2
- Validation: Pydantic
- Testing: pytest
- Packaging and execution: uv, Uvicorn
- Linting: ruff

## Architecture Overview

The application is organized into clear layers for maintainability and extensibility:

- app/main.py: application entry point and router configuration
- app/api/: API endpoints and page routes
- app/services/: business logic for student operations
- app/models/: database entities and relationships
- app/schemas/: request and response validation models
- templates/ and static/: frontend presentation layer
- tests/: automated regression and CRUD coverage

This structure reflects a thoughtful approach to software design that is easy to extend as the product grows.

## Project Goals

The primary goal of this project is to showcase:

- Strong Python backend development skills
- A solid understanding of API and database integration
- Professional code organization and maintainability
- The ability to build a usable application from concept to implementation

## Prerequisites

To run this project locally, you will need:

- Python 3.12+
- uv
- PostgreSQL running locally or available through Docker

## Environment Setup

Create a .env file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/hyper_scale_ops
APP_PORT=8000
DEBUG_MODE=true
```

## Installation

```bash
uv sync
```

## Running the Application

Start the development server:

```bash
uv run uvicorn app.main:app --reload
```

Open the app in your browser:

- http://127.0.0.1:8000/ for the landing page
- http://127.0.0.1:8000/students for the student management view

## Database Migrations

Apply the latest schema changes:

```bash
uv run alembic upgrade head
```

Create a new migration when the models change:

```bash
uv run alembic revision --autogenerate -m "your message"
```

## API Surface

The backend exposes a clean REST API for student operations:

- GET /healthcheck/{name}
- GET /db-check
- GET /api/v1/all-students
- GET /api/v1/fetch-one-student/{student_id}
- POST /api/v1/new-student
- PUT /api/v1/modify-student/{student_id}
- DELETE /api/v1/delete-student/{student_id}

## Testing and Quality Assurance

The project includes automated tests for the main CRUD flow and error handling scenarios:

```bash
ENV_FILE=.env.test uv run pytest
```

This demonstrates attention to reliability, regression prevention, and maintainable software delivery.

## Development Workflow

Useful commands include:

```bash
make install
make run
make migration msg='message'
make upgrade
make run-pytest
make docker_start
```

## Docker Support

The application can also be containerized for easier deployment and testing:

```bash
docker build -t my-project-img:v1 .
docker run -d --name my-project-cont --env-file .env -p 8000:8000 my-project-img:v1
```

## Summary

Hyper Scale Ops is more than a demo application. It reflects a practical, professional approach to building software that is easy to understand, maintain, and evolve. It is well suited for showcasing backend engineering ability, API design judgment, and strong development habits to recruiters and technical managers.
