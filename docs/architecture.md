# 🏗️ Architecture du Système

## Vue d'Ensemble

Le système Fear & Greed Index est une application full-stack qui calcule et expose un indice de sentiment du marché boursier marocain.

```
┌─────────────────┐
│   Frontend      │  React + TypeScript
│   (Port 8080)   │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│   Backend API   │  FastAPI + Python
│   (Port 8001)   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │         │          │          │
┌───▼───┐ ┌──▼───┐  ┌───▼───┐  ┌───▼───┐
│ SQLite│ │Redis │  │Scrapers│ │Scheduler│
│   DB  │ │Cache │  │        │ │ APScheduler│
└───────┘ └──────┘  └────────┘ └─────────┘
```

---

## Composants Principaux

### 1. Backend API (FastAPI)

**Responsabilités** :
- Exposer les endpoints REST
- Calculer l'indice Fear & Greed
- Gérer le scraping des médias
- Orchestrer les pipelines de traitement
- Gérer l'authentification et la sécurité

**Structure** :
```
app/
├── api/              # Endpoints REST
├── core/             # Configuration, logging, monitoring
├── models/           # Modèles de données (SQLAlchemy)
├── pipelines/        # Pipelines de traitement
│   ├── ingestion/    # Scrapers web
│   └── processing/   # Calculs des composantes
├── services/          # Services métier
└── utils/            # Utilitaires
```

### 2. Frontend (React + TypeScript)

**Responsabilités** :
- Afficher le dashboard
- Visualiser les données historiques
- Gérer l'interface utilisateur
- Appeler l'API backend

**Technologies** :
- React 18+
- TypeScript
- Tailwind CSS
- Recharts (graphiques)

### 3. Base de Données

**SQLite (Développement)** :
- Tables : `index_scores`, `media_articles`
- Migrations : Alembic

**PostgreSQL (Production)** :
- Support TimescaleDB pour time-series
- Optimisations pour grandes quantités de données

### 4. Cache (Redis)

**Responsabilités** :
- Cache des requêtes API
- Cache des résultats de scraping
- Amélioration des performances

**Fallback** : Cache en mémoire si Redis indisponible

### 5. Scrapers

**Sources** :
- Hespress
- Medias24
- BourseNews

**Technologies** :
- BeautifulSoup
- Selenium (pour sites avec JavaScript)
- Cloudscraper (pour bypass anti-bot)

### 6. Scheduler (APScheduler)

**Responsabilités** :
- Exécuter le pipeline toutes les 10 minutes
- Gérer les jobs récurrents
- Contrôle via API

---

## Flux de Données

### Calcul de l'Indice

```
1. Scheduler déclenche le pipeline
   │
2. Pipeline Service orchestre
   │
3. Market Scraper → Données MASI
   │
4. Media Scraper → Articles médias
   │
5. Sentiment Analysis → Scores sentiment
   │
6. Component Calculator → 6 composantes
   │
7. Aggregator → Score final (0-100)
   │
8. Sauvegarde en DB
   │
9. Cache mis à jour
```

### Requête API

```
1. Client → API Endpoint
   │
2. Rate Limiting Middleware
   │
3. Metrics Middleware (tracking)
   │
4. Authentication (si nécessaire)
   │
5. Business Logic (Service)
   │
6. Database Query (avec cache)
   │
7. Response → Client
```

---

## Sécurité

### Authentification

- **JWT** : Tokens pour l'authentification
- **Bcrypt** : Hash des mots de passe
- **Rate Limiting** : Protection contre les abus

### Configuration

- **SECRET_KEY** : Clé secrète pour JWT
- **CORS** : Origines autorisées
- **HTTPS** : En production (recommandé)

---

## Monitoring

### Métriques Prometheus

- Requêtes HTTP (total, durée, erreurs)
- Requêtes base de données
- Opérations de scraping
- Opérations de cache
- Exécutions de pipeline

### Health Checks

- `/monitoring/health` : Santé complète
- `/monitoring/health/database` : Santé DB
- `/monitoring/stats` : Statistiques

### Logging

- **Structuré** : JSON (production)
- **Standard** : Texte (développement)
- **Niveaux** : DEBUG, INFO, WARNING, ERROR

---

## Scalabilité

### Horizontal

- **Load Balancer** : Distribuer les requêtes
- **Multiple Instances** : Backend stateless
- **Database Replication** : Pour la DB

### Vertical

- **Cache Redis** : Réduire la charge DB
- **Optimisation Queries** : Index, pagination
- **Async Processing** : Jobs en arrière-plan

---

## Déploiement

### Développement

```bash
# Backend
uvicorn app.main:app --reload

# Frontend
npm run dev
```

### Production

```bash
# Docker
docker-compose up -d

# Ou avec scripts
./start_all.sh
```

---

## Technologies

### Backend

- **FastAPI** : Framework web
- **SQLAlchemy** : ORM
- **Alembic** : Migrations
- **APScheduler** : Scheduler
- **Prometheus** : Métriques
- **Redis** : Cache

### Frontend

- **React** : Framework UI
- **TypeScript** : Type safety
- **Tailwind CSS** : Styling
- **Recharts** : Graphiques

### Infrastructure

- **SQLite/PostgreSQL** : Base de données
- **Redis** : Cache
- **Docker** : Conteneurisation
- **Nginx** : Reverse proxy (optionnel)

---

## Patterns Utilisés

### Repository Pattern

Services abstraient l'accès aux données.

### Dependency Injection

FastAPI gère les dépendances automatiquement.

### Middleware Pattern

- Rate limiting
- Metrics tracking
- CORS

### Factory Pattern

Création de scrapers selon la source.

---

## Performance

### Optimisations

- **Cache** : Réduit les requêtes DB
- **Pagination** : Limite les données retournées
- **Async** : Traitement non-bloquant
- **Connection Pooling** : Réutilise les connexions DB

### Métriques Cibles

- **Latence API** : < 200ms (P95)
- **Throughput** : > 100 req/s
- **Cache Hit Rate** : > 70%

---

## Évolutivité

### Ajouter une Source

1. Créer un scraper dans `pipelines/ingestion/`
2. Ajouter à `SOURCE_LISTINGS` dans `enhanced_media_service.py`
3. Tester et déployer

### Ajouter une Composante

1. Créer le calculateur dans `pipelines/processing/`
2. Ajouter au `ComponentCalculator`
3. Mettre à jour les poids dans `metadata`
4. Créer une migration si nécessaire

### Ajouter un Endpoint

1. Créer le fichier dans `api/v1/endpoints/`
2. Ajouter au router
3. Documenter dans `docs/API.md`

---

**📖 Pour plus de détails, consultez les autres documents dans `docs/`.**
