"""
Rate limiting pour protéger l'API contre les abus
"""
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import time

from app.core.config import settings
from app.core.logging import get_logger
from app.services.cache_service import get_cache_service

logger = get_logger(__name__)
cache_service = get_cache_service()


class RateLimiter:
    """
    Rate limiter utilisant Redis (ou mémoire) pour limiter les requêtes par IP
    """
    
    def __init__(
        self,
        requests_per_minute: Optional[int] = None,
        requests_per_hour: Optional[int] = None
    ):
        """
        Args:
            requests_per_minute: Nombre de requêtes par minute (défaut: depuis config)
            requests_per_hour: Nombre de requêtes par heure (défaut: depuis config)
        """
        self.requests_per_minute = requests_per_minute or settings.rate_limit_per_minute
        self.requests_per_hour = requests_per_hour or settings.rate_limit_per_hour
    
    def get_client_ip(self, request: Request) -> str:
        """
        Récupère l'IP du client depuis la requête
        
        Args:
            request: Requête FastAPI
        
        Returns:
            IP du client
        """
        # Vérifier les headers de proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Prendre la première IP (client original)
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback sur l'IP directe
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def check_rate_limit(self, request: Request) -> tuple[bool, Optional[dict]]:
        """
        Vérifie si la requête respecte les limites de taux
        
        Args:
            request: Requête FastAPI
        
        Returns:
            Tuple (is_allowed, rate_limit_info)
            - is_allowed: True si la requête est autorisée
            - rate_limit_info: Dict avec les infos de limite (si refusé)
        """
        if not settings.rate_limit_enabled:
            return True, None
        
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # Clés de cache
        minute_key = f"rate_limit:minute:{client_ip}"
        hour_key = f"rate_limit:hour:{client_ip}"
        
        # Vérifier la limite par minute
        minute_count = cache_service.get(minute_key) or 0
        if minute_count >= self.requests_per_minute:
            return False, {
                "limit_type": "minute",
                "limit": self.requests_per_minute,
                "retry_after": 60 - int(current_time % 60)
            }
        
        # Vérifier la limite par heure
        hour_count = cache_service.get(hour_key) or 0
        if hour_count >= self.requests_per_hour:
            return False, {
                "limit_type": "hour",
                "limit": self.requests_per_hour,
                "retry_after": 3600 - int(current_time % 3600)
            }
        
        # Incrémenter les compteurs
        cache_service.set(minute_key, minute_count + 1, ttl_seconds=60)
        cache_service.set(hour_key, hour_count + 1, ttl_seconds=3600)
        
        return True, None
    
    async def __call__(self, request: Request):
        """
        Middleware FastAPI pour le rate limiting
        
        Args:
            request: Requête FastAPI
        
        Raises:
            HTTPException: Si la limite est dépassée
        """
        is_allowed, rate_limit_info = self.check_rate_limit(request)
        
        if not is_allowed:
            retry_after = rate_limit_info.get("retry_after", 60)
            limit = rate_limit_info.get("limit", 0)
            limit_type = rate_limit_info.get("limit_type", "minute")
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {limit} requests per {limit_type}",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + retry_after)
                }
            )
        
        return None


# Instance globale du rate limiter
rate_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Retourne l'instance globale du rate limiter"""
    return rate_limiter



