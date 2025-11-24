# 💻 Guide de Développement

## Structure du Projet

```
casablanca-stock/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints API
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/             # Configuration, logging, monitoring
│   │   ├── models/           # Modèles de données
│   │   ├── pipelines/        # Pipelines de traitement
│   │   │   ├── ingestion/   # Scrapers
│   │   │   └── processing/  # Calculs
│   │   ├── services/         # Services métier
│   │   └── utils/            # Utilitaires
│   ├── alembic/              # Migrations
│   ├── scripts/               # Scripts utilitaires
│   └── tests/                 # Tests
│
├── frontend/                  # Application frontend
│   └── src/
│       ├── pages/            # Pages
│       ├── components/       # Composants React
│       └── lib/              # Utilitaires
│
└── docs/                     # Documentation
```

---

## Workflow de Développement

### 1. Créer une Branche

```bash
git checkout -b feature/nouvelle-fonctionnalite
```

### 2. Développer

```bash
# Activer l'environnement virtuel
cd backend
source .venv/bin/activate

# Lancer en mode développement
uvicorn app.main:app --reload
```

### 3. Tests

```bash
# Tests unitaires
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Tests avec couverture
pytest --cov=app tests/
```

### 4. Linting & Formatage

```bash
# Linting
ruff check app/

# Formatage
black app/

# Type checking (si mypy configuré)
mypy app/
```

### 5. Migrations

```bash
# Créer une migration
python scripts/migrate.py autogenerate "description"

# Appliquer
python scripts/migrate.py upgrade
```

### 6. Commit

```bash
git add .
git commit -m "feat: nouvelle fonctionnalité"
```

---

## Ajouter un Nouvel Endpoint

### 1. Créer le Fichier Endpoint

```python
# backend/app/api/v1/endpoints/nouveau.py
from fastapi import APIRouter, Depends
from app.api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/nouveau", summary="Nouvel endpoint")
async def nouveau_endpoint(db: Session = Depends(get_db)):
    return {"message": "Hello"}
```

### 2. Ajouter au Router

```python
# backend/app/api/v1/router.py
from .endpoints import nouveau

api_router.include_router(nouveau.router, prefix="/nouveau", tags=["Nouveau"])
```

---

## Ajouter une Migration

### 1. Modifier le Modèle

```python
# backend/app/models/schemas.py
class MediaArticle(Base):
    # ... colonnes existantes ...
    nouvelle_colonne = Column(String, nullable=True)
```

### 2. Générer la Migration

```bash
python scripts/migrate.py autogenerate "add nouvelle_colonne"
```

### 3. Vérifier et Appliquer

```bash
# Vérifier le fichier généré dans alembic/versions/
# Puis appliquer
python scripts/migrate.py upgrade
```

---

## Ajouter un Nouveau Scraper

### 1. Créer le Scraper

```python
# backend/app/pipelines/ingestion/nouveau_scraper.py
from app.pipelines.ingestion.enhanced_media_scraper import EnhancedMediaScraper

class NouveauScraper(EnhancedMediaScraper):
    def __init__(self):
        super().__init__()
        self.source_name = "nouveau"
    
    async def scrape_article(self, url: str) -> EnhancedMediaArticle:
        # Implémenter le scraping
        pass
```

### 2. Intégrer dans le Service

```python
# backend/app/services/enhanced_media_service.py
from app.pipelines.ingestion.nouveau_scraper import NouveauScraper

SOURCE_LISTINGS = {
    # ... sources existantes ...
    "nouveau": [
        "https://example.com/articles"
    ]
}
```

---

## Ajouter des Métriques

### 1. Utiliser les Helpers Existants

```python
from app.core.monitoring import track_scraping, scraping_requests_total

with track_scraping("nouvelle_source"):
    # Code de scraping
    scraping_requests_total.labels(source="nouvelle_source", status="success").inc()
```

### 2. Créer de Nouvelles Métriques

```python
# backend/app/core/monitoring.py
nouvelle_metrique = Counter(
    'nouvelle_metrique_total',
    'Description',
    ['label1', 'label2']
)
```

---

## Logging

### Utilisation Standard

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

logger.info("Message d'information")
logger.warning("Avertissement")
logger.error("Erreur", exc_info=True)
```

### Logging Structuré

```python
from app.core.logging import get_structured_logger

logger = get_structured_logger(__name__)

logger.bind(
    article_id=123,
    source="hespress"
).info("Article traité")
```

---

## Tests

### Structure des Tests

```
tests/
├── unit/              # Tests unitaires
│   ├── test_services.py
│   └── test_models.py
└── integration/       # Tests d'intégration
    ├── test_api.py
    └── test_pipeline.py
```

### Exemple de Test

```python
# tests/unit/test_services.py
import pytest
from app.services.enhanced_media_service import EnhancedMediaService

@pytest.mark.asyncio
async def test_scrape_all_sources():
    service = EnhancedMediaService()
    result = await service.scrape_all_sources()
    assert result["total_scraped"] > 0
```

### Exécuter les Tests

```bash
# Tous les tests
pytest

# Tests spécifiques
pytest tests/unit/test_services.py

# Avec couverture
pytest --cov=app --cov-report=html
```

---

## Debugging

### Backend

```python
# Utiliser le debugger Python
import pdb; pdb.set_trace()

# Ou utiliser ipdb (plus avancé)
import ipdb; ipdb.set_trace()
```

### Frontend

```javascript
// Utiliser le debugger du navigateur
debugger;

// Console logs
console.log("Debug:", data);
```

### Logs

```bash
# Backend
tail -f logs/backend.log

# Frontend
tail -f logs/frontend.log
```

---

## Performance

### Profiling

```python
# Profiling Python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code à profiler
# ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Monitoring

```bash
# Voir les métriques
curl http://localhost:8001/api/v1/monitoring/metrics

# Health check
curl http://localhost:8001/api/v1/monitoring/health
```

---

## Code Style

### Python

- **PEP 8** : Style guide Python
- **Black** : Formatage automatique
- **Ruff** : Linting rapide
- **Type hints** : Annotations de type

### Exemple

```python
from typing import Optional, List

def process_articles(
    articles: List[dict],
    limit: Optional[int] = None
) -> List[dict]:
    """Traite une liste d'articles.
    
    Args:
        articles: Liste des articles à traiter
        limit: Nombre maximum d'articles (None = tous)
    
    Returns:
        Liste des articles traités
    """
    if limit:
        articles = articles[:limit]
    return articles
```

---

## Git Workflow

### Branches

- `main` : Production
- `develop` : Développement
- `feature/*` : Nouvelles fonctionnalités
- `fix/*` : Corrections de bugs
- `docs/*` : Documentation

### Messages de Commit

Format : `type: description`

Types :
- `feat` : Nouvelle fonctionnalité
- `fix` : Correction de bug
- `docs` : Documentation
- `style` : Formatage
- `refactor` : Refactoring
- `test` : Tests
- `chore` : Maintenance

Exemples :
```
feat: add new scraper for medias24
fix: resolve database connection issue
docs: update API documentation
```

---

## Déploiement

### Préparation

```bash
# Tests
pytest

# Linting
ruff check app/
black --check app/

# Migrations
python scripts/migrate.py current
```

### Build

```bash
# Backend
cd backend
docker build -t fear-greed-backend .

# Frontend
cd frontend
npm run build
docker build -t fear-greed-frontend .
```

---

## Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**💡 Astuce** : Utilisez `http://localhost:8001/docs` pour tester les endpoints pendant le développement.



