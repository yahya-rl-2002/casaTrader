# 📚 Documentation API Complète

## Vue d'Ensemble

L'API Fear & Greed Index expose des endpoints REST pour accéder aux données de l'indice, aux composantes, aux articles médias, et pour contrôler le système.

**Base URL** : `http://localhost:8001/api/v1`

**Documentation Interactive** : `http://localhost:8001/docs` (Swagger UI)

---

## 🔐 Authentification

### Endpoints d'Authentification

#### POST `/auth/login`
Connexion et obtention d'un token JWT.

**Request Body** :
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### GET `/auth/me`
Récupère les informations de l'utilisateur connecté.

**Headers** :
```
Authorization: Bearer <token>
```

**Response** :
```json
{
  "username": "admin",
  "user_id": 1,
  "role": null
}
```

#### GET `/auth/verify`
Vérifie la validité d'un token.

**Headers** :
```
Authorization: Bearer <token>
```

**Response** :
```json
{
  "valid": true,
  "username": "admin",
  "user_id": 1
}
```

---

## 📊 Index & Scores

### GET `/index/latest`
Récupère le dernier score de l'indice Fear & Greed.

**Response** :
```json
{
  "as_of": "2025-11-15",
  "score": 65.5
}
```

### GET `/index/history`
Récupère l'historique des scores.

**Query Parameters** :
- `range` (optional): `30d`, `90d`, `180d`, `1y`, `all`
- `start_date` (optional): Date de début (format: YYYY-MM-DD)
- `end_date` (optional): Date de fin (format: YYYY-MM-DD)

**Example** :
```bash
GET /api/v1/index/history?range=90d
```

**Response** :
```json
{
  "data": [
    {
      "as_of": "2025-11-15",
      "score": 65.5
    },
    {
      "as_of": "2025-11-14",
      "score": 63.2
    }
  ]
}
```

---

## 🧩 Composantes

### GET `/components/latest`
Récupère les dernières valeurs des 6 composantes.

**Response** :
```json
{
  "as_of": "2025-11-15",
  "momentum": 70.5,
  "price_strength": 65.0,
  "volume": 55.2,
  "volatility": 60.8,
  "equity_vs_bonds": 58.3,
  "media_sentiment": 72.1
}
```

---

## 📈 Formule Simplifiée

### GET `/simplified-v2/score`
Récupère le score simplifié (Volume + Sentiment + Performance) / 76.

**Response** :
```json
{
  "score": 65.5,
  "as_of": "2025-11-15",
  "components": {
    "volume": 55.2,
    "sentiment": 72.1,
    "performance": 68.3
  },
  "calculation": {
    "formula": "(volume + sentiment + performance) / 76",
    "raw_sum": 165.6,
    "normalized_score": 65.5
  }
}
```

### GET `/simplified-v2/details`
Récupère les détails complets du calcul simplifié.

**Response** :
```json
{
  "score": 65.5,
  "as_of": "2025-11-15",
  "components": {
    "volume": {
      "value": 55.2,
      "contribution": 18.2
    },
    "sentiment": {
      "value": 72.1,
      "contribution": 23.8
    },
    "performance": {
      "value": 68.3,
      "contribution": 22.5
    }
  },
  "metadata": {
    "calculation_method": "simplified_v2",
    "data_points": 252
  }
}
```

---

## 📰 Médias & Articles

### GET `/media/latest`
Récupère les derniers articles médias avec sentiment.

**Query Parameters** :
- `limit` (optional, default: 20): Nombre d'articles (1-500)
- `offset` (optional, default: 0): Offset pour pagination
- `cursor` (optional): Cursor pour pagination basée sur ID
- `auto_scrape` (optional, default: false): Scraper automatiquement si articles anciens

**Example** :
```bash
GET /api/v1/media/latest?limit=10&offset=0
```

**Response** :
```json
{
  "articles": [
    {
      "title": "Titre de l'article",
      "summary": "Résumé...",
      "content": "Contenu complet...",
      "url": "https://example.com/article",
      "source": "hespress",
      "image_url": "https://example.com/image.jpg",
      "published_at": "2025-11-15T10:00:00",
      "sentiment_score": 0.65,
      "sentiment_label": "positive"
    }
  ],
  "pagination": {
    "total": 100,
    "limit": 10,
    "offset": 0,
    "has_more": true
  }
}
```

### GET `/media/sources`
Liste toutes les sources de médias disponibles.

**Response** :
```json
{
  "sources": [
    {
      "name": "hespress",
      "display_name": "Hespress",
      "url": "https://fr.hespress.com/economie",
      "article_count": 42
    },
    {
      "name": "medias24",
      "display_name": "Medias24",
      "url": "https://medias24.com/economie",
      "article_count": 35
    }
  ]
}
```

### GET `/media/sentiment-stats`
Statistiques de sentiment des articles.

**Response** :
```json
{
  "total_articles": 100,
  "sentiment_distribution": {
    "positive": 45,
    "negative": 30,
    "neutral": 25
  },
  "average_sentiment": 0.55,
  "by_source": {
    "hespress": {
      "total": 42,
      "average_sentiment": 0.58
    }
  }
}
```

### POST `/media/trigger-scraping`
Déclenche un scraping manuel des articles.

**Response** :
```json
{
  "success": true,
  "message": "Scraping démarré en arrière-plan",
  "job_id": "scraping_20251115_143000"
}
```

### POST `/media/sync-to-supabase`
Synchronise les articles vers Supabase.

**Query Parameters** :
- `sources` (optional): Liste des sources à synchroniser
- `limit` (optional): Nombre maximum d'articles

**Example** :
```bash
POST /api/v1/media/sync-to-supabase?sources=hespress,medias24&limit=100
```

---

## 📊 Volume & Trading

### GET `/volume/latest`
Récupère les données de volume pour la heatmap.

**Query Parameters** :
- `days` (optional, default: 30): Nombre de jours (7-90)

**Response** :
```json
{
  "data": [
    {
      "date": "2025-11-15",
      "volume": 1250000,
      "normalized": 0.75
    }
  ],
  "stats": {
    "min": 500000,
    "max": 2000000,
    "average": 1250000
  }
}
```

### GET `/volume/stats`
Statistiques de volume.

**Response** :
```json
{
  "total_volume": 50000000,
  "average_daily": 1250000,
  "trend": "increasing"
}
```

### GET `/volume/trend`
Tendance du volume.

**Response** :
```json
{
  "trend": "increasing",
  "change_percent": 15.5,
  "period": "30d"
}
```

---

## 🔄 Pipeline

### POST `/pipeline/run`
Exécute le pipeline complet de calcul de l'indice.

**Query Parameters** :
- `target_date` (optional): Date cible (format: YYYY-MM-DD)

**Response** :
```json
{
  "success": true,
  "message": "Pipeline completed successfully",
  "final_score": 65.5,
  "target_date": "2025-11-15"
}
```

### POST `/pipeline/run-background`
Exécute le pipeline en arrière-plan.

**Response** :
```json
{
  "success": true,
  "message": "Pipeline started in background",
  "job_id": "pipeline_20251115_143000"
}
```

### GET `/pipeline/status`
Statut du pipeline.

**Response** :
```json
{
  "status": "running",
  "current_step": "media_scraping",
  "progress": 0.65
}
```

---

## ⏰ Scheduler

### GET `/scheduler/status`
Statut du scheduler et des jobs.

**Response** :
```json
{
  "running": true,
  "jobs": [
    {
      "id": "index_update_10min",
      "next_run": "2025-11-15T14:40:00",
      "status": "scheduled"
    }
  ]
}
```

### POST `/scheduler/trigger`
Déclenche un job manuellement.

**Query Parameters** :
- `job_id` (optional): ID du job à déclencher

**Response** :
```json
{
  "success": true,
  "message": "Job triggered successfully",
  "job_id": "index_update_10min"
}
```

### POST `/scheduler/configure`
Configure le scheduler.

**Request Body** :
```json
{
  "interval_minutes": 5,
  "enabled": true
}
```

---

## 🧪 Backtest

### GET `/backtest/run`
Exécute un backtest de corrélation.

**Query Parameters** :
- `range` (optional, default: "90d"): Période (`30d`, `90d`, `180d`, `1y`)

**Response** :
```json
{
  "period": "90d",
  "correlation_t1": 0.65,
  "correlation_t5": 0.72,
  "mean_return_t1": 0.02,
  "mean_return_t5": 0.05,
  "data_points": 90
}
```

---

## 📊 Monitoring

### GET `/monitoring/health`
Health check complet du système.

**Response** :
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
      "misses": 567
    }
  },
  "scheduler": {
    "status": "running",
    "active_jobs": 2
  }
}
```

### GET `/monitoring/metrics`
Métriques Prometheus.

**Response** : Format Prometheus (texte)

### GET `/monitoring/stats`
Statistiques détaillées du système.

**Response** :
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
    "active_jobs": 2
  }
}
```

---

## 🔧 Cache

### GET `/media/cache/stats`
Statistiques du cache.

**Response** :
```json
{
  "hits": 1234,
  "misses": 567,
  "hit_rate": 0.68,
  "size": 100
}
```

### DELETE `/media/cache/clear`
Vide le cache.

**Query Parameters** :
- `pattern` (optional): Pattern à supprimer (ex: `volume:*`)

**Response** :
```json
{
  "success": true,
  "cleared_keys": 42,
  "pattern": "volume:*"
}
```

---

## 📋 Métadonnées

### GET `/metadata/weights`
Pondérations des composantes.

**Response** :
```json
{
  "momentum": 0.25,
  "price_strength": 0.25,
  "volume": 0.15,
  "volatility": 0.15,
  "equity_vs_bonds": 0.10,
  "media_sentiment": 0.10
}
```

### GET `/metadata/components`
Liste des composantes.

**Response** :
```json
{
  "components": [
    "momentum",
    "price_strength",
    "volume",
    "volatility",
    "equity_vs_bonds",
    "media_sentiment"
  ]
}
```

---

## 🏥 Health

### GET `/health/ping`
Ping simple.

**Response** :
```json
{
  "status": "ok"
}
```

---

## ⚠️ Codes d'Erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Accès refusé |
| 404 | Ressource non trouvée |
| 429 | Rate limit dépassé |
| 500 | Erreur serveur |

---

## 🔒 Rate Limiting

Par défaut :
- **60 requêtes par minute** par IP
- **1000 requêtes par heure** par IP

Headers de réponse :
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
Retry-After: 15
```

---

## 📝 Exemples d'Utilisation

### Récupérer le dernier score
```bash
curl http://localhost:8001/api/v1/index/latest
```

### Récupérer les articles avec pagination
```bash
curl "http://localhost:8001/api/v1/media/latest?limit=10&offset=0"
```

### Déclencher un scraping
```bash
curl -X POST http://localhost:8001/api/v1/media/trigger-scraping
```

### Se connecter et utiliser le token
```bash
# Connexion
TOKEN=$(curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

# Utiliser le token
curl http://localhost:8001/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

**📖 Documentation Interactive** : http://localhost:8001/docs



