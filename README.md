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

## High-Level Architecture

```mermaid
---
config:
  fontFamily: Verdana, Geneva, sans-serif
  theme: neo-dark
  look: handDrawn
  flowchart:
    curve: basis
    nodeSpacing: 45
    rankSpacing: 80
---

flowchart LR

%% ==========================
%% Developer
%% ==========================

subgraph DEV["👨‍💻 Developer"]
    PY["🐍 Python 3.12"]
    UV["⚡ uv"]
    IDE["💻 PyCharm Pro"]
    POSTMAN["📬 Postman"]
    GIT["🌿 Git"]
end

%% ==========================
%% Source Control
%% ==========================

subgraph SCM["☁️ Source Control"]
    GH["GitHub"]
end

%% ==========================
%% CI/CD
%% ==========================

subgraph CICD["🚀 GitHub Actions"]
    LINT["Ruff"]
    TEST["Pytest"]
    BUILD["Docker Build"]
    PUSH["Push Image"]
end

%% ==========================
%% Registry
%% ==========================

subgraph REG["📦 Container Registry"]
    HUB["Docker Hub"]
end

%% ==========================
%% Kubernetes
%% ==========================

subgraph K8S["☸️ Kubernetes Cluster"]

    INGRESS["NGINX Ingress"]

    subgraph APP["Hyper-Scale-Ops"]

        POD1["FastAPI Pod"]
        POD2["FastAPI Pod"]

        HELM["Helm Chart"]

    end

end

%% ==========================
%% Database
%% ==========================

subgraph DB["🗄️ PostgreSQL"]

    DEVDB["dev"]

    TESTDB["test"]

    PYTEST["pytest"]

    PROD["prod"]

end

%% ==========================
%% Observability
%% ==========================

subgraph OBS["📈 Observability"]

    OTEL["OpenTelemetry"]

    PROM["Prometheus"]

    GRAF["Grafana"]

    DD["Datadog"]

end

%% ==========================
%% Secret Management
%% ==========================

subgraph SEC["🔐 Secret Management"]

    GHSEC["GitHub Secrets"]

    K8SSEC["Kubernetes Secrets"]

    VAULT["HashiCorp Vault (Planned)"]

end

%% ==========================
%% Flow
%% ==========================

PY --> UV
IDE --> GIT
POSTMAN --> INGRESS

GIT --> GH

GH --> LINT
LINT --> TEST
TEST --> BUILD
BUILD --> PUSH
PUSH --> HUB

HUB --> HELM
HELM --> POD1
HELM --> POD2

INGRESS --> POD1
INGRESS --> POD2

POD1 --> DEVDB
POD1 --> TESTDB
POD1 --> PYTEST
POD1 --> PROD

POD2 --> DEVDB
POD2 --> TESTDB
POD2 --> PYTEST
POD2 --> PROD

POD1 --> OTEL
POD2 --> OTEL

OTEL --> PROM
PROM --> GRAF
OTEL --> DD

GHSEC --> BUILD
K8SSEC --> POD1
K8SSEC --> POD2
VAULT -. Future .-> POD1
VAULT -. Future .-> POD2

%% ==========================
%% Styling
%% ==========================

classDef dev fill:#E3F2FD,stroke:#1565C0,stroke-width:2,color:#000;
classDef ci fill:#FFF8E1,stroke:#EF6C00,stroke-width:2,color:#000;
classDef app fill:#E8F5E9,stroke:#2E7D32,stroke-width:2,color:#000;
classDef db fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2,color:#000;
classDef obs fill:#FFF3E0,stroke:#E65100,stroke-width:2,color:#000;
classDef sec fill:#FCE4EC,stroke:#AD1457,stroke-width:2,color:#000;

class PY,UV,IDE,POSTMAN,GIT,GH dev
class LINT,TEST,BUILD,PUSH,HUB ci
class INGRESS,POD1,POD2,HELM app
class DEVDB,TESTDB,PYTEST,PROD db
class OTEL,PROM,GRAF,DD obs
class GHSEC,K8SSEC,VAULT sec

```


## CI/CD pipeline

```mermaid
---
config:
  theme: neo-dark
  fontFamily: Verdana, Geneva, sans-serif
  look: handDrawn
---

flowchart TB

subgraph SCM["Source Control"]
    DEV["Developer"]
    GIT["GitHub"]
end

subgraph CI["Continuous Integration"]

    PR["Pull Request"]

    LINT["Ruff"]

    TEST["Pytest"]

    BUILD["Docker Build"]

end

subgraph REG["Container Registry"]

    HUB["Docker Hub"]

end

subgraph CD["Continuous Deployment"]

    HELM["Helm Upgrade"]

    K8S["Kubernetes"]

end

subgraph APP["Application"]

    POD["FastAPI Pods"]

end

DEV --> GIT

GIT --> PR

PR --> LINT

LINT --> TEST

TEST --> BUILD

BUILD --> HUB

HUB --> HELM

HELM --> K8S

K8S --> POD


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
      🟢 MicroK8s
      🟢 Helm
      🟢 NGINX Ingress

    Cloud
      🟢 Domain
      🟢 SSL
      🟢 Heroku
      ⚪ AWS
      🟢 DigitalOcean
```


## Git Branching Strategy

```mermaid
---
title: Hyper-Scale-Ops Git Branching Strategy
config:
  theme: neo-dark
  fontFamily: Verdana, Geneva, sans-serif
  look: handDrawn
  flowchart:
    curve: basis
    rankSpacing: 70
    nodeSpacing: 50
---

gitGraph
    commit id: "Project Init"

    branch feature/student-service
    checkout feature/student-service
    commit id: "Student CRUD"
    commit id: "Unit Tests"
    checkout main
    merge feature/student-service

    branch feature/teacher-service
    checkout feature/teacher-service
    commit id: "Teacher APIs"
    checkout main
    merge feature/teacher-service

    branch feature/helm
    checkout feature/helm
    commit id: "Helm Chart"
    commit id: "Ingress"
    checkout main
    merge feature/helm

    branch dev-deploy
    checkout dev-deploy
    commit id: "Deploy to Dev Server"

    checkout main
    commit id: "Production Release"
```


## Database Design (ER Diagram)

```mermaid
---
title: Hyper-Scale-Ops ER Diagram
config:
  theme: neo-dark
  fontFamily: Verdana, Geneva, sans-serif
  look: handDrawn
  flowchart:
    curve: basis
    rankSpacing: 70
    nodeSpacing: 50
---

erDiagram
    classes ||--o{ students : "has many"
    classes ||--o{ periods : "schedules"
    teachers ||--o{ periods : "teaches"
    students ||--|| student_details : "has explicit profile (1:1)"
    
    classes {
        int id PK "autoincrement"
        string name "String(50)"
        int level
        datetime created_at
        datetime updated_at
    }

    students {
        int id PK "autoincrement"
        string name "String(255)"
        string phone_number "String(20)"
        string roll_number UK "String(50)"
        int class_id FK "nullable"
        datetime created_at
        datetime updated_at
    }

    student_details {
        int id PK "autoincrement"
        int student_id FK, UK "ondelete=CASCADE"
        string address_line_1 "String(255)"
        string address_line_2 "String(255), nullable"
        string state "String(100)"
        string father_name "String(255)"
        datetime created_at
        datetime updated_at
    }

    teachers {
        int id PK "autoincrement"
        string name "String(255)"
        string phone_number "String(20)"
        string subject "String(100)"
        datetime created_at
        datetime updated_at
    }

    periods {
        int id PK "autoincrement"
        int class_id FK
        int teacher_id FK
        string day "String(20)"
        time start_time
        time end_time
        datetime created_at
        datetime updated_at
    }

    alembic_version {
        string version_num PK "String(32)"
    }
```



## Kubernetes Architecture

```mermaid
---
title: Hyper-Scale-Ops Kubernetes Architecture
config:
  theme: neo-dark
  fontFamily: Verdana, Geneva, sans-serif
  look: handDrawn
  flowchart:
    curve: basis
    rankSpacing: 70
    nodeSpacing: 50
---

flowchart TB

%% =====================
%% External
%% =====================

USER["👤 User"]

DNS["🌍 DNS<br/>adityalive.tech"]

TLS["🔒 Let's Encrypt<br/>cert-manager"]

USER --> DNS
DNS --> TLS

%% =====================
%% Cluster
%% =====================

subgraph CLUSTER["☸️ Kubernetes Cluster"]

ING["NGINX Ingress"]

SVC["ClusterIP Service"]

DEP["Deployment"]

POD1["FastAPI Pod #1"]

POD2["FastAPI Pod #2"]

CM["ConfigMap"]

SECRET["Secret"]

end

TLS --> ING

ING --> SVC

SVC --> DEP

DEP --> POD1
DEP --> POD2

CM --> POD1
CM --> POD2

SECRET --> POD1
SECRET --> POD2

%% =====================
%% Database
%% =====================

subgraph DB["🗄 Oracle Cloud"]

PG["PostgreSQL"]

end

POD1 --> PG
POD2 --> PG

%% =====================
%% Helm
%% =====================

subgraph HELM["📦 Helm"]

CHART["Chart.yaml"]

VALUES["values.yaml"]

ENV["Environment Values<br/>dev / test / prod"]

TEMPLATE["Templates"]

end

CHART --> TEMPLATE
VALUES --> TEMPLATE
ENV --> TEMPLATE

TEMPLATE -. deploy .-> DEP

%% =====================
%% CI/CD
%% =====================

subgraph CICD["⚙️ CI/CD"]

GH["GitHub"]

ACTION["GitHub Actions"]

REG["Docker Hub"]

end

GH --> ACTION
ACTION --> REG
REG --> DEP

%% =====================
%% Observability
%% =====================

subgraph OBS["📈 Observability"]

OTEL["OpenTelemetry"]

PROM["Prometheus"]

GRAF["Grafana"]

DD["Datadog"]

end

POD1 --> OTEL
POD2 --> OTEL

OTEL --> PROM
PROM --> GRAF

OTEL --> DD
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
