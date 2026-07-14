## 📊 Live Links

<p align="center">

<a href="https://dev.adityalive.tech/">
    <img src="https://img.shields.io/badge/🚀-Live%20Application-430098?style=for-the-badge" />
</a>

<a href="https://p.us5.datadoghq.com/sb/8e9bd3b1-7001-11f1-aae3-c2753782a27a-994485ddc16ff7de20d382368a9bf932">
    <img src="https://img.shields.io/badge/📈-Live%20Datadog%20Dashboard-632CA6?style=for-the-badge&logo=datadog&logoColor=white" />
</a>

</p>

<p align="center">
<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&height=4&color=0:334155,100:475569"/>
</p>

# Hyper Scale Ops

Hyper Scale Ops is a modern full-stack web application (I used jinja2 templates for frontend) designed to demonstrate strong backend engineering, clean API design, and practical product thinking. The project showcases a student management system that combines a FastAPI-powered backend, database-driven business logic, and a simple user-facing interface suitable for internal tools or lightweight operational workflows.

This README is written with a recruiter and technical manager audience in mind, highlighting not just what the project does, but how it is built, how it scales in structure, and how it reflects professional software development practices.

## Current Architecture

```mermaid
---
config:
  fontFamily: Verdana, Geneva, sans-serif
  theme: neo-dark
  look: handDrawn
---
%%{init: {
    "theme":"base",
    "themeVariables":{
        "fontSize":"38px"
    },
    "flowchart": {
        "rankSpacing": 330,
        "nodeSpacing": 50
    },
    "themeCSS": ".pyBlock polygon, [class*='pyBlock'] rect { fill: #FFD43B !important; background-color: #FFD43B !important; stroke: #306998 !important; stroke-width: 4px !important; color: #306998 !important; }"
}}%%
flowchart LR
subgraph DEV["🟩 DEVELOPER WORKSTATION"]
PY[Python]:::pyBlock
UV[uv]
PC[PyCharm Pro]
PM[Postman]
GIT[Git]
end

subgraph SCM["🟩 SOURCE CONTROL"]
GH[GitHub]
end

subgraph CI["🟩 JENKINS CI/CD"]
J[Jenkins]
R[Ruff]
T[Pytest]
B[Build Docker Image]
DH[Push Docker Image]
N1[Slack Notification]
N2[Email Notification]
end

subgraph REG["🟩 CONTAINER REGISTRY"]
HUB[Docker Hub]
end

subgraph CLOUD["🟩 HEROKU"]
HEROKU[Heroku]
DOMAIN[dev.adityalive.tech]
SSL[SSL HTTPS]
end

subgraph APP["🟩 FASTAPI APPLICATION"]
API[FastAPI]
ASYNC[Async]
PYD[Pydantic]
SQLA[SQLAlchemy Async]
ALE[Alembic]
JINJA[Jinja2]
end

subgraph DB["🟩 ORACLE CLOUD POSTGRESQL"]
DEV1[dev1]
DEV2[dev2]
TEST[test]
PYTESTDB[pytest]
PROD[prod]
end

subgraph OBS["🟩 OBSERVABILITY"]
DD[Datadog]
end

PY-->UV-->API
PC-->API
PM-->API
GIT-->GH-->J
J-->R-->T-->B-->DH-->HUB
HUB-->HEROKU
HEROKU-->DOMAIN-->SSL
API-->ASYNC
API-->PYD
API-->SQLA
API-->ALE
API-->JINJA
SQLA-->DEV1
SQLA-->DEV2
SQLA-->TEST
SQLA-->PYTESTDB
SQLA-->PROD
API-->DD
T-->N1
T-->N2

```


## CI/CD pipeline

```mermaid
---
config:
  theme: neo-dark
  fontFamily: Verdana, Geneva, sans-serif
  look: handDrawn
---
flowchart LR
DEV[Developer]-->GH[GitHub]
GH-->J[Jenkins]
J-->L[Ruff]
L-->P[Pytest]
P-->D[Build Docker Image]
D-->H[Push to Docker Hub]
H-->HEROKU[Deploy to Heroku]
HEROKU-->LIVE[dev.adityalive.tech]
J-->S[Slack Notification]
J-->E[Email Notification]


```

## Technology Stack & Implementation Roadmap

> **Legend:** 🟢 Completed · ⚪ Upcoming
```mermaid
%%{init:{
"theme":"dark",
"themeVariables":{
"fontSize":"18px",
"lineColor":"#9CA3AF"
},
"themeCSS":"

g.mindmap-node.depth-0 circle{
fill:#374151!important;
stroke:#9CA3AF!important;
stroke-width:3px!important;
}

g.mindmap-node.section-0 .mindmap-node-rect{
fill:#22C55E!important;
stroke:#15803D!important;
}

g.mindmap-node.section-1 .mindmap-node-rect{
fill:#F59E0B!important;
stroke:#D97706!important;
}

g.mindmap-node.section-2 .mindmap-node-rect{
fill:#3B82F6!important;
stroke:#2563EB!important;
}

.mindmap-node text{
fill:white!important;
font-size:18px!important;
font-weight:bold!important;
}

path.mindmap-edge{
stroke:#9CA3AF!important;
stroke-width:4px!important;
}

"
}}%%

mindmap
  root((Hyper Scale Ops))

    Backend
      🟢 FastAPI
      🟢 Async / Await
      🟢 SQLAlchemy
      🟢 Alembic
      🟢 Pydantic
      🟢 Jinja2
      🟢 PostgreSQL

    Containers
      🟢 Docker
      🟢 Docker Hub
      🟢 Multi-stage Builds
      🟢 Image Optimization

    Database
      Oracle Cloud PostgreSQL
        🟢 dev
        🟢 test
        🟢 pytest
        🟢 prod


    CI/CD
      🟢 Jenkins
      🟢 GitHub Actions
      🟢 Ruff
      🟢 Multi-stage Pipelines
      🟢 Email Notifications
      🟢 Slack Notifications
      ⚪ Trivy
      ⚪ Sentry
      🟢 Pytest
      ⚪ BrowserStack


    Observability
      ⚪ OpenTelemetry
      🟢 Datadog
      ⚪ Prometheus
      ⚪ Grafana
      ⚪ New Relic

    Kubernetes
      ⚪ MicroK8s
      ⚪ Helm
      ⚪ NGINX Ingress

    Cloud
      🟢 Domain
      🟢 SSL
      🟢 Heroku
      ⚪ AWS
      ⚪ DigitalOcean
```

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
