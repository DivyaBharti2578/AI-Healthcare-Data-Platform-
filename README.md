# 🏥 AI-Powered Healthcare Data Platform

A **production-style healthcare analytics backend** that converts **natural language queries into validated SQL** executed on a structured healthcare data warehouse.

The platform simulates **enterprise healthcare data engineering systems**, demonstrating backend API development, AI-assisted query generation, and containerized data infrastructure.

---

# 🚀 Overview

This project simulates an **enterprise healthcare analytics platform** integrating:

• **PostgreSQL** (containerized healthcare warehouse)  
• **FastAPI backend** for API services  
• **LLM-powered SQL generation** using Llama3 via Ollama  
• **Schema-constrained prompting** for reliable SQL generation  
• **SQL validation & sanitization pipeline**  
• **Automated data quality monitoring**  
• **Query logging and execution observability**  
• **Docker Compose orchestration**

The architecture mirrors **real-world healthcare data engineering systems used in organizations like CVS Health and UnitedHealth Group**.

---

# 🏗 System Architecture
User Query
↓
FastAPI Backend
↓
LLM SQL Generator (Llama3 / Ollama)
↓
SQL Validation Layer
↓
PostgreSQL Healthcare Warehouse
↓
Query Results


---

# 🐳 Dockerized Services

| Service | Description |
|-------|-------------|
| backend | FastAPI application + AI SQL engine |
| db | PostgreSQL healthcare database |

The system runs using **Docker Compose for reproducible environments**.

---

# 📊 Data Model

The platform uses a **star-schema inspired healthcare warehouse**.

### Fact Table

`fact_claims`

### Dimension Tables

`dim_member`  
`dim_provider`

The system generates **50,000+ synthetic healthcare claims** using the **Faker library** to simulate enterprise-scale datasets.

---


The system automatically:

1️⃣ Converts the question into SQL  
2️⃣ Validates the SQL  
3️⃣ Executes it safely on PostgreSQL  
4️⃣ Returns the analytics results

---

# 🛡 AI Safety & Query Validation

To prevent unsafe or malicious queries the system implements:

• Schema-constrained SQL generation  
• SQL sanitization (removes markdown / explanations)  
• Destructive query blocking (`DROP`, `DELETE`, `TRUNCATE`)  
• Query validation before execution  
• Retry logic for database connection failures  
• Container-safe database connection lifecycle

---

# 📈 Observability & Data Governance

The platform includes a **query observability framework**.

### Query Logging

A dedicated logging table records:

• Executed SQL  
• Query execution time  
• Query timestamps  
• API request metadata

---

### Data Quality Monitoring

Automated checks run on healthcare data including:

• Null value detection  
• Negative value detection  
• Future-dated claims detection

This simulates **data governance pipelines used in healthcare analytics platforms**.

---

# ⚙ Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Backend development |
| FastAPI | REST API framework |
| PostgreSQL | Healthcare data warehouse |
| Docker | Containerized deployment |
| Docker Compose | Multi-service orchestration |
| Ollama + Llama3 | AI-powered SQL generation |
| Faker | Synthetic healthcare data generation |

---

# ▶ Running the Project

Clone the repository:
git clone https://github.com/DivyaBharti2578/AI-Healthcare-Data-Platform
