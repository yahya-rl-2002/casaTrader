# CasaTrader Backend API

## Overview
Backend FastAPI pour **CasaTrader** - Plateforme complète d'investissement boursier pour la Bourse de Casablanca. 

Ce backend fournit :
- **Fear & Greed Index** : Calcul de l'indice de sentiment du marché
- **Scraping de rapports financiers** : Téléchargement automatique des rapports de 55+ entreprises
- **Analyse de sentiment** : NLP et LLM pour analyser les actualités financières
- **API REST complète** : Endpoints pour toutes les fonctionnalités de la plateforme

## Features
- ✅ **Modular pipelines** for data ingestion, feature engineering, and aggregation
- ✅ **Async SQLAlchemy** integration with SQLite (dev) and PostgreSQL (prod)
- ✅ **Background scheduling** with APScheduler for automatic updates
- ✅ **NLP sentiment analysis** with spaCy and OpenAI LLM support
- ✅ **Pydantic schemas** and typed services for maintainability
- ✅ **JWT Authentication** with rate limiting
- ✅ **Prometheus metrics** for monitoring
- ✅ **Redis caching** with memory fallback
- ✅ **Alembic migrations** for database management
- ✅ **Structured logging** with JSON support
- ✅ **Health checks** and system monitoring

## Getting Started
1. Install Poetry: https://python-poetry.org/docs/
2. Install dependencies:
   ```bash
   cd backend
   poetry install
   ```
3. Run development server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
4. Access interactive docs at `http://localhost:8000/docs`.

## Project Structure
- `app/api`: FastAPI routers, dependencies, versioned endpoints.
- `app/core`: Configuration and logging utilities.
- `app/models`: Database session factory and Pydantic schemas.
- `app/pipelines`: Ingestion and processing pipelines plus aggregator.
- `app/services`: Sentiment, scaling, and scheduler services.
- `app/tasks`: Background jobs orchestrating daily index computation.
- `app/utils`: Reusable helpers for HTTP requests, parsing, validation.

## Environment Variables
Copy `.env.example` to `.env` and customize:

```
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/fear_greed
TIMESCALE_ENABLED=true
SCHEDULER_TZ=Africa/Casablanca
SCHEDULER_DAILY_RUN=16:00
```

## Tests & Linting
```bash
poetry run pytest
poetry run ruff check app
poetry run black app --check
```

## Documentation

- **[API Documentation](../docs/API.md)** - Complete API reference
- **[Installation Guide](../docs/INSTALLATION.md)** - Setup instructions
- **[Development Guide](../docs/DEVELOPMENT.md)** - Developer guide
- **[Architecture](../docs/ARCHITECTURE.md)** - System architecture
- **[Monitoring](../MONITORING.md)** - Monitoring and observability
- **[Migrations](../MIGRATIONS.md)** - Database migrations guide
- **[Security](../SECURITE.md)** - Security documentation

## Interactive API Docs

Access the interactive API documentation at:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python scripts/migrate.py upgrade

# Start server
uvicorn app.main:app --reload
```

## Roadmap
- ✅ Database models and migrations (Alembic) - **DONE**
- ✅ Authentication & rate limiting - **DONE**
- ✅ Monitoring and metrics - **DONE**
- ✅ Caching with Redis - **DONE**
- 🔜 TimescaleDB hypertables for time-series storage
- 🔜 Expand test coverage
- 🔜 WebSocket support for real-time updates



