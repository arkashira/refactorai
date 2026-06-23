# TECH_SPEC.md – RefactorAI

---

## 1. Overview

**RefactorAI** is a lightweight analytics engine that aggregates refactoring actions performed across multiple repositories, computes weekly code‑quality metrics, and exposes a simple API for dashboards and reporting.  
The system is designed to run as a background service or as a library embedded in CI/CD pipelines.

---

## 2. Architecture

```
┌───────────────────────┐
│  Client / Dashboard   │
│  (REST / GraphQL API) │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  RefactorAI Service    │
│  (Python 3.11)         │
│  ├─ RefactorAI Core    │
│  │  ├─ Action Store    │
│  │  ├─ Metric Engine   │
│  │  └─ Exporter        │
│  └─ Auth / Rate‑Limit  │
└───────┬───────────────┘
        │
        ▼
┌───────────────────────┐
│  PostgreSQL 15         │
│  (Primary DB)          │
│  ├─ actions            │
│  ├─ metrics_weekly     │
│  └─ users              │
└───────────────────────┘
```

* **Client** – Web dashboard, CLI, or any consumer that talks to the REST/GraphQL API.  
* **RefactorAI Service** – Stateless FastAPI application.  
* **PostgreSQL** – Persistent storage for actions, users, and pre‑computed weekly metrics.  
* **Background Workers** – Celery workers recompute weekly metrics nightly.  
* **Auth** – API key based authentication stored in `users` table.  

---

## 3. Data Model

| Table | Columns | Description |
|-------|---------|-------------|
| `users` | `id (PK)`, `api_key (unique)`, `created_at` | API keys for authentication. |
| `actions` | `id (PK)`, `org`, `repo`, `score (float)`, `effort (float)`, `performed_at (timestamp)`, `created_at` | Raw refactoring actions. |
| `metrics_weekly` | `id (PK)`, `org`, `repo`, `week_start (date)`, `avg_score`, `total_effort`, `action_count`, `created_at` | Aggregated weekly metrics. |

*All timestamps are UTC.*

---

## 4. Core Components

| Component | Responsibility | Key Methods |
|-----------|----------------|-------------|
| **RefactorAI** | Public API wrapper | `add_action`, `get_weekly_metrics`, `export_csv`, `authenticate` |
| **ActionStore** | Persist actions | `insert(action)`, `query_by_repo(org, repo, start, end)` |
| **MetricEngine** | Compute weekly aggregates | `recompute_week(org, repo, week_start)`, `get_weekly(org, repo)` |
| **Exporter** | CSV/JSON export | `to_csv(metrics)`, `to_json(metrics)` |
| **AuthMiddleware** | API key validation | `validate(api_key)` |

---

## 5. Key APIs / Interfaces

### 5.1 REST Endpoints (FastAPI)

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| POST | `/actions` | Add a refactoring action | `RefactoringAction` JSON | 201 Created |
| GET | `/metrics/week` | Get weekly metrics | `org`, `repo`, `week_start` (query) | `WeeklyMetrics` JSON |
| GET | `/export/csv` | Export metrics as CSV | `org`, `repo`, `start`, `end` | CSV file |
| POST | `/auth` | Authenticate API key | `api_key` | 200 OK / 401 |

### 5.2 Python Library

```python
from refactor_ai import RefactorAI, RefactoringAction
from datetime import datetime

refactor_ai = RefactorAI(api_key="YOUR_KEY")

# Add action
refactor_ai.add_action(
    RefactoringAction(
        org="org1",
        repo="repo1",
        score=0.8,
        effort=10.0,
        performed_at=datetime(2022, 1, 3)
    )
)

# Get weekly metrics
metrics = refactor_ai.get_weekly_metrics(org="org1", repo="repo1", week_start="2022-01-03")

# Export CSV
csv_data = refactor_ai.export_csv(org="org1", repo="repo1", start="2022-01-01", end="2022-02-01")
```

---

## 6. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Language** | Python 3.11 | Mature ecosystem, async support |
| **Web Framework** | FastAPI | Fast, async, built‑in OpenAPI |
| **Database** | PostgreSQL 15 | ACID, JSONB support, good for time series |
| **ORM** | SQLAlchemy 2.0 | Declarative models, async support |
| **Background Jobs** | Celery 5.3 + Redis | Periodic recomputation |
| **Auth** | API Key + JWT (optional) | Simple, stateless |
| **Deployment** | Docker + Docker‑Compose | Reproducible environments |
| **CI/CD** | GitHub Actions | Automated tests & image build |
| **Testing** | pytest + httpx | Unit & integration tests |
| **Monitoring** | Prometheus + Grafana | Metrics on request latency, DB health |
| **Logging** | Loguru | Structured logs |

---

## 7. Dependencies

```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.111.0"
uvicorn = "^0.30.0"
sqlalchemy = "^2.0.30"
asyncpg = "^0.29.0"
pydantic = "^2.8.0"
celery = "^5.4.0"
redis = "^5.0.0"
loguru = "^0.7.2"
python-dotenv = "^1.0.0"

[tool.poetry.dev-dependencies]
pytest = "^8.3.0"
httpx = "^0.27.0"
pytest-asyncio = "^0.23.0"
```

All dependencies are open‑source and MIT/Apache‑2.0 licensed.

---

## 8. Deployment

### 8.1 Docker Compose

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: refactor
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: refactor_ai
    volumes:
      - db_data:/var/lib/postgresql/data
  redis:
    image: redis:7
  api:
    build: .
    command: uvicorn refactor_ai.main:app --host 0.0.0.0 --port 8000
    environment:
      DATABASE_URL: postgres://refactor:secret@db:5432/refactor_ai
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis
  worker:
    build: .
    command: celery -A refactor_ai.celery_app worker --loglevel=info
    environment:
      DATABASE_URL: postgres://refactor:secret@db:5432/refactor_ai
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - db
      - redis
volumes:
  db_data:
```

### 8.2 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@localhost:5432/db` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `API_KEY` | Default API key for initial access | *None* (must be created via DB) |
| `LOG_LEVEL` | Logging level | `INFO` |

### 8.3 CI Pipeline

1. **Lint** – `ruff check .`
2. **Test** – `pytest`
3. **Build Docker** – `docker build -t refactorai:latest .`
4. **Push** – to Docker Hub or ECR
5. **Deploy** – via Helm or plain Docker Compose

---

## 9. Security Considerations

| Area | Mitigation |
|------|------------|
| API Key Exposure | Store in env var, rotate via DB |
| SQL Injection | Use SQLAlchemy ORM, parameterized queries |
| Rate Limiting | `slowapi` middleware, Redis counter |
| Data Encryption | TLS for API, encrypted connection to Postgres |
| Secrets Management | Use Vault or AWS Secrets Manager in production |

---

## 10. Future Enhancements

1. **GraphQL API** – for more flexible queries.  
2. **Webhook Integration** – push metrics to external dashboards.  
3. **Multi‑tenant Isolation** – separate schemas per org.  
4. **Advanced Metrics** – churn, defect density correlation.  
5. **UI Dashboard** – React + Vite, hosted on S3+CloudFront.

---

## 11. Contact & Support

- **Repository**: `arkashira/refactorai`  
- **Issue Tracker**: GitHub Issues  
- **Slack**: `#refactorai` (internal)  
- **Email**: support@axentx.io

---
