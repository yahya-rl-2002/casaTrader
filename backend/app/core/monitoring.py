"""
Monitoring et observabilité
- Métriques Prometheus
- Logging structuré
- Health checks
"""
import time
from typing import Optional
from contextlib import contextmanager
from functools import wraps

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import Response as FastAPIResponse

from app.core.logging import get_logger

logger = get_logger(__name__)

# ============================================================================
# MÉTRIQUES PROMETHEUS
# ============================================================================

# Compteurs de requêtes HTTP
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

# Durée des requêtes HTTP
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# Requêtes actives
http_requests_in_flight = Gauge(
    'http_requests_in_flight',
    'Number of HTTP requests currently being processed',
    ['method', 'endpoint']
)

# Erreurs
http_errors_total = Counter(
    'http_errors_total',
    'Total number of HTTP errors',
    ['method', 'endpoint', 'error_type']
)

# Métriques de base de données
db_queries_total = Counter(
    'db_queries_total',
    'Total number of database queries',
    ['operation', 'table']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table'],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

# Métriques de scraping
scraping_requests_total = Counter(
    'scraping_requests_total',
    'Total number of scraping requests',
    ['source', 'status']
)

scraping_duration_seconds = Histogram(
    'scraping_duration_seconds',
    'Scraping duration in seconds',
    ['source'],
    buckets=(1.0, 2.5, 5.0, 10.0, 15.0, 30.0, 60.0, 120.0)
)

# Métriques de cache
cache_hits_total = Counter(
    'cache_hits_total',
    'Total number of cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total number of cache misses',
    ['cache_type']
)

cache_operations_total = Counter(
    'cache_operations_total',
    'Total number of cache operations',
    ['operation', 'cache_type']
)

# Métriques de pipeline
pipeline_runs_total = Counter(
    'pipeline_runs_total',
    'Total number of pipeline runs',
    ['status']
)

pipeline_duration_seconds = Histogram(
    'pipeline_duration_seconds',
    'Pipeline execution duration in seconds',
    buckets=(10.0, 30.0, 60.0, 120.0, 300.0, 600.0)
)

# Métriques de sentiment
sentiment_analyses_total = Counter(
    'sentiment_analyses_total',
    'Total number of sentiment analyses',
    ['method', 'status']
)

sentiment_analysis_duration_seconds = Histogram(
    'sentiment_analysis_duration_seconds',
    'Sentiment analysis duration in seconds',
    ['method'],
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0)
)

# Métriques système
system_info = Gauge(
    'system_info',
    'System information',
    ['version', 'environment']
)

# ============================================================================
# HELPERS POUR MÉTRIQUES
# ============================================================================

@contextmanager
def track_http_request(method: str, endpoint: str):
    """Context manager pour tracker une requête HTTP"""
    http_requests_in_flight.labels(method=method, endpoint=endpoint).inc()
    start_time = time.time()
    
    try:
        yield
    finally:
        duration = time.time() - start_time
        http_requests_in_flight.labels(method=method, endpoint=endpoint).dec()
        http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)


@contextmanager
def track_db_query(operation: str, table: str):
    """Context manager pour tracker une requête DB"""
    start_time = time.time()
    
    try:
        yield
    finally:
        duration = time.time() - start_time
        db_queries_total.labels(operation=operation, table=table).inc()
        db_query_duration_seconds.labels(operation=operation, table=table).observe(duration)


@contextmanager
def track_scraping(source: str):
    """Context manager pour tracker un scraping"""
    start_time = time.time()
    
    try:
        yield
    finally:
        duration = time.time() - start_time
        scraping_duration_seconds.labels(source=source).observe(duration)


def track_cache_hit(cache_type: str):
    """Tracker un cache hit"""
    cache_hits_total.labels(cache_type=cache_type).inc()
    cache_operations_total.labels(operation='hit', cache_type=cache_type).inc()


def track_cache_miss(cache_type: str):
    """Tracker un cache miss"""
    cache_misses_total.labels(cache_type=cache_type).inc()
    cache_operations_total.labels(operation='miss', cache_type=cache_type).inc()


def track_cache_set(cache_type: str):
    """Tracker un cache set"""
    cache_operations_total.labels(operation='set', cache_type=cache_type).inc()


def track_cache_delete(cache_type: str):
    """Tracker un cache delete"""
    cache_operations_total.labels(operation='delete', cache_type=cache_type).inc()


def track_pipeline_run(status: str = "success"):
    """Tracker une exécution de pipeline"""
    pipeline_runs_total.labels(status=status).inc()


def track_sentiment_analysis(method: str, status: str = "success"):
    """Tracker une analyse de sentiment"""
    sentiment_analyses_total.labels(method=method, status=status).inc()


# ============================================================================
# MIDDLEWARE POUR TRACKING
# ============================================================================

async def metrics_middleware(request: Request, call_next):
    """Middleware pour tracker les métriques HTTP"""
    method = request.method
    endpoint = request.url.path
    
    # Normaliser l'endpoint (enlever les IDs)
    normalized_endpoint = normalize_endpoint(endpoint)
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        
        # Tracker la requête
        http_requests_total.labels(
            method=method,
            endpoint=normalized_endpoint,
            status_code=status_code
        ).inc()
        
        # Tracker les erreurs
        if status_code >= 400:
            error_type = get_error_type(status_code)
            http_errors_total.labels(
                method=method,
                endpoint=normalized_endpoint,
                error_type=error_type
            ).inc()
        
        return response
        
    except Exception as e:
        # Tracker les exceptions
        http_errors_total.labels(
            method=method,
            endpoint=normalized_endpoint,
            error_type=type(e).__name__
        ).inc()
        raise
    
    finally:
        duration = time.time() - start_time
        http_request_duration_seconds.labels(
            method=method,
            endpoint=normalized_endpoint
        ).observe(duration)


def normalize_endpoint(endpoint: str) -> str:
    """Normalise un endpoint en remplaçant les IDs par des placeholders"""
    import re
    # Remplacer les IDs numériques
    endpoint = re.sub(r'/\d+', '/{id}', endpoint)
    # Remplacer les UUIDs
    endpoint = re.sub(
        r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
        '/{uuid}',
        endpoint,
        flags=re.IGNORECASE
    )
    return endpoint


def get_error_type(status_code: int) -> str:
    """Détermine le type d'erreur à partir du code de statut"""
    if 400 <= status_code < 500:
        return "client_error"
    elif 500 <= status_code < 600:
        return "server_error"
    else:
        return "unknown_error"


# ============================================================================
# ENDPOINT PROMETHEUS
# ============================================================================

def get_metrics_response() -> FastAPIResponse:
    """Retourne les métriques Prometheus"""
    return FastAPIResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )



