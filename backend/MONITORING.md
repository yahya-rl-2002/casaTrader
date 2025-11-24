# 📊 Monitoring et Observabilité

## ✅ Implémentation Complète

Le système dispose maintenant d'un système complet de monitoring et observabilité avec :
- **Métriques Prometheus** pour le monitoring des performances
- **Logging structuré** pour une meilleure traçabilité
- **Health checks avancés** pour la surveillance de l'état du système
- **Endpoints de monitoring** pour l'intégration avec des outils externes

---

## 📋 Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── monitoring.py      # Métriques Prometheus et helpers
│   │   └── logging.py         # Logging structuré amélioré
│   └── api/v1/endpoints/
│       └── monitoring.py       # Endpoints de monitoring
└── MONITORING.md              # Cette documentation
```

---

## 🎯 Métriques Prometheus

### Métriques HTTP

- **`http_requests_total`** : Nombre total de requêtes HTTP (par méthode, endpoint, status)
- **`http_request_duration_seconds`** : Durée des requêtes HTTP (histogramme)
- **`http_requests_in_flight`** : Nombre de requêtes en cours
- **`http_errors_total`** : Nombre d'erreurs HTTP (par type)

### Métriques Base de Données

- **`db_queries_total`** : Nombre total de requêtes DB (par opération, table)
- **`db_query_duration_seconds`** : Durée des requêtes DB (histogramme)

### Métriques Scraping

- **`scraping_requests_total`** : Nombre de requêtes de scraping (par source, status)
- **`scraping_duration_seconds`** : Durée des scrapings (histogramme)

### Métriques Cache

- **`cache_hits_total`** : Nombre de cache hits
- **`cache_misses_total`** : Nombre de cache misses
- **`cache_operations_total`** : Nombre total d'opérations cache (par opération, type)

### Métriques Pipeline

- **`pipeline_runs_total`** : Nombre d'exécutions de pipeline (par status)
- **`pipeline_duration_seconds`** : Durée d'exécution du pipeline

### Métriques Sentiment

- **`sentiment_analyses_total`** : Nombre d'analyses de sentiment (par méthode, status)
- **`sentiment_analysis_duration_seconds`** : Durée des analyses de sentiment

---

## 🔌 Endpoints de Monitoring

### 1. Métriques Prometheus

**GET** `/api/v1/monitoring/metrics`

Retourne les métriques au format Prometheus.

```bash
curl http://localhost:8001/api/v1/monitoring/metrics
```

**Exemple de réponse** :
```
# HELP http_requests_total Total number of HTTP requests
# TYPE http_requests_total counter
http_requests_total{endpoint="/api/v1/media/latest",method="GET",status_code="200"} 42.0
http_request_duration_seconds_bucket{endpoint="/api/v1/media/latest",method="GET",le="0.005"} 35.0
...
```

### 2. Health Check Complet

**GET** `/api/v1/monitoring/health`

Vérifie la santé complète du système :
- Statut général de l'API
- Connexion à la base de données
- Statut du cache
- Statut du scheduler

```bash
curl http://localhost:8001/api/v1/monitoring/health
```

**Exemple de réponse** :
```json
{
  "overall": {
    "status": "healthy",
    "timestamp": "2025-11-15T14:30:00",
    "version": "0.1.0",
    "environment": "development",
    "uptime_seconds": 3600.5
  },
  "database": {
    "status": "healthy",
    "response_time_ms": 2.5
  },
  "cache": {
    "status": "available",
    "stats": {
      "hits": 1234,
      "misses": 567,
      "size": 100
    }
  },
  "scheduler": {
    "status": "running",
    "active_jobs": 2,
    "jobs": [
      {
        "id": "index_update_10min",
        "next_run": "2025-11-15T14:40:00"
      }
    ]
  }
}
```

### 3. Health Check Base de Données

**GET** `/api/v1/monitoring/health/database`

Vérifie uniquement la santé de la base de données.

```bash
curl http://localhost:8001/api/v1/monitoring/health/database
```

### 4. Ping Simple

**GET** `/api/v1/monitoring/health/ping`

Ping simple pour vérifier que l'API répond (utilisé par les load balancers).

```bash
curl http://localhost:8001/api/v1/monitoring/health/ping
```

### 5. Statistiques du Système

**GET** `/api/v1/monitoring/stats`

Statistiques détaillées du système :
- Statistiques de la base de données
- Statistiques du cache
- Statistiques du scheduler

```bash
curl http://localhost:8001/api/v1/monitoring/stats
```

**Exemple de réponse** :
```json
{
  "timestamp": "2025-11-15T14:30:00",
  "database": {
    "media_articles_count": 1234,
    "index_scores_count": 567,
    "latest_score": {
      "score": 65.5,
      "as_of": "2025-11-15T14:00:00"
    }
  },
  "cache": {
    "hits": 1234,
    "misses": 567,
    "hit_rate": 0.68
  },
  "scheduler": {
    "active_jobs": 2,
    "jobs": [
      {
        "id": "index_update_10min",
        "next_run": "2025-11-15T14:40:00"
      }
    ]
  }
}
```

---

## 🔧 Utilisation dans le Code

### Tracker une Requête HTTP

Le middleware `metrics_middleware` track automatiquement toutes les requêtes HTTP. Aucune action nécessaire.

### Tracker une Requête DB

```python
from app.core.monitoring import track_db_query

with track_db_query("SELECT", "media_articles"):
    articles = db.query(MediaArticle).all()
```

### Tracker un Scraping

```python
from app.core.monitoring import track_scraping, scraping_requests_total

with track_scraping("hespress"):
    # Code de scraping
    scraping_requests_total.labels(source="hespress", status="success").inc()
```

### Tracker le Cache

```python
from app.core.monitoring import track_cache_hit, track_cache_miss, track_cache_set

# Dans cache_service.py
if cached_value:
    track_cache_hit("media")
    return cached_value
else:
    track_cache_miss("media")
    # ... calculer la valeur ...
    track_cache_set("media")
    return value
```

### Tracker le Pipeline

```python
from app.core.monitoring import track_pipeline_run, pipeline_duration_seconds
import time

start_time = time.time()
try:
    # Exécuter le pipeline
    result = run_pipeline()
    track_pipeline_run("success")
except Exception as e:
    track_pipeline_run("error")
    raise
finally:
    duration = time.time() - start_time
    pipeline_duration_seconds.observe(duration)
```

---

## 📊 Intégration avec Prometheus

### Configuration Prometheus

Ajoutez cette configuration dans `prometheus.yml` :

```yaml
scrape_configs:
  - job_name: 'fear-greed-api'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/api/v1/monitoring/metrics'
```

### Grafana Dashboard

Créez un dashboard Grafana avec les métriques suivantes :

1. **Requêtes HTTP par seconde**
   ```
   rate(http_requests_total[5m])
   ```

2. **Latence P95 des requêtes**
   ```
   histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
   ```

3. **Taux d'erreur**
   ```
   rate(http_errors_total[5m]) / rate(http_requests_total[5m])
   ```

4. **Cache hit rate**
   ```
   rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))
   ```

5. **Durée du pipeline**
   ```
   histogram_quantile(0.95, rate(pipeline_duration_seconds_bucket[5m]))
   ```

---

## 📝 Logging Structuré

### Configuration

Le logging structuré peut être activé via les settings :

```python
# Dans app/core/config.py
logging_json_format: bool = False  # Activer pour JSON
logging_level: str = "INFO"
```

### Utilisation

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

# Logging standard
logger.info("Processing article", extra={
    "article_id": article.id,
    "source": article.source
})

# Avec structlog (si disponible)
logger = get_structured_logger(__name__)
logger.bind(article_id=article.id, source=article.source).info("Processing article")
```

---

## 🚨 Alertes Recommandées

### Alertes Critiques

1. **API Down**
   ```
   up{job="fear-greed-api"} == 0
   ```

2. **Taux d'erreur élevé**
   ```
   rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.05
   ```

3. **Latence élevée**
   ```
   histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1.0
   ```

4. **Base de données inaccessible**
   ```
   monitoring_database_status{status="unhealthy"} == 1
   ```

### Alertes de Performance

1. **Cache hit rate faible**
   ```
   rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m])) < 0.5
   ```

2. **Pipeline lent**
   ```
   histogram_quantile(0.95, rate(pipeline_duration_seconds_bucket[5m])) > 300
   ```

3. **Scraping échouant**
   ```
   rate(scraping_requests_total{status="error"}[5m]) > 0
   ```

---

## 🔍 Dépannage

### Métriques non visibles

**Problème** : Les métriques n'apparaissent pas dans Prometheus

**Solutions** :
1. Vérifier que le middleware est activé dans `app/main.py`
2. Vérifier l'endpoint `/api/v1/monitoring/metrics`
3. Vérifier la configuration Prometheus

### Health check échoue

**Problème** : Le health check retourne "unhealthy"

**Solutions** :
1. Vérifier les logs pour les erreurs spécifiques
2. Vérifier la connexion à la base de données
3. Vérifier la configuration du cache
4. Vérifier le scheduler

### Performance dégradée

**Problème** : Les métriques montrent une performance dégradée

**Solutions** :
1. Analyser les métriques de latence
2. Vérifier le cache hit rate
3. Vérifier les requêtes DB lentes
4. Vérifier les scrapings qui échouent

---

## 📚 Ressources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [Structlog Documentation](https://www.structlog.org/)

---

**Date**: 2025-11-15  
**Version**: 1.0.0  
**Statut**: ✅ Implémenté et Opérationnel



