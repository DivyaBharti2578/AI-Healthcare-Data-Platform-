# AI-Powered Healthcare Data Platform

Production-style backend service that translates natural language healthcare queries into validated SQL executed over a structured claims data warehouse.

## 🚀 Overview

This project simulates an enterprise healthcare analytics platform integrating:

- PostgreSQL (containerized)
- FastAPI backend
- LLM-powered SQL generation (Llama3 via Ollama)
- Schema-constrained prompting
- SQL validation & sanitization
- Data quality framework
- Query logging & execution monitoring
- Docker Compose orchestration

Designed to reflect real-world healthcare data engineering workflows similar to enterprise environments such as CVS Health.

---

## 🏗 Architecture

User → FastAPI → LLM (Ollama) → PostgreSQL


Dockerized Services:
- `backend` – FastAPI + AI SQL engine
- `db` – PostgreSQL database

---

## 📊 Data Model

Star-schema inspired healthcare warehouse:

- `fact_claims`
- `dim_member`
- `dim_provider`

50K+ synthetic claims generated using Faker to simulate enterprise-scale datasets.

---

## 🛡 AI Safety & Robustness

- Schema-constrained SQL generation
- SQL sanitization (removes markdown/explanations)
- Destructive query blocking (DROP, DELETE, etc.)
- Retry logic for failed DB connections
- Environment-variable based configuration
- Container-safe DB connection lifecycle

---

## 📈 Observability & Data Governance

- Query logging table (tracks SQL, execution time, timestamps)
- Automated data quality validation:
  - Null checks
  - Negative value detection
  - Future-dated claims detection
- API request latency logging middleware

---

## 🐳 Run Locally (Docker)

```bash
docker compose up --build


### API Docs:

http://localhost:8000/docs

### Health Check:

http://localhost:8000/health