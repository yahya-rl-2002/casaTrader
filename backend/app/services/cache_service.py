"""
Service de cache Redis centralisé pour améliorer les performances
"""
from __future__ import annotations

import json
import pickle
from typing import Any, Optional
from datetime import timedelta
import redis
from redis.exceptions import ConnectionError, TimeoutError

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CacheService:
    """
    Service de cache Redis avec fallback en mémoire si Redis n'est pas disponible
    """
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialise le service de cache
        
        Args:
            redis_url: URL Redis (ex: redis://localhost:6379/0)
                     Si None, utilise REDIS_URL de la config ou fallback en mémoire
        """
        self.redis_url = redis_url or getattr(settings, 'redis_url', None)
        self.redis_client: Optional[redis.Redis] = None
        self.memory_cache: dict[str, tuple[Any, float]] = {}  # Fallback en mémoire
        self.use_redis = False
        
        # Tenter de se connecter à Redis
        if self.redis_url:
            try:
                self.redis_client = redis.from_url(
                    self.redis_url,
                    decode_responses=False,  # On gère nous-mêmes la sérialisation
                    socket_connect_timeout=2,
                    socket_timeout=2,
                    retry_on_timeout=True,
                    health_check_interval=30
                )
                # Test de connexion
                self.redis_client.ping()
                self.use_redis = True
                logger.info(f"✅ Redis connecté: {self.redis_url}")
            except (ConnectionError, TimeoutError, Exception) as e:
                logger.warning(f"⚠️  Redis non disponible ({e}), utilisation du cache en mémoire")
                self.redis_client = None
                self.use_redis = False
        else:
            logger.info("ℹ️  Redis URL non configurée, utilisation du cache en mémoire")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur du cache
        
        Args:
            key: Clé du cache
            default: Valeur par défaut si la clé n'existe pas
            
        Returns:
            Valeur en cache ou default
        """
        if self.use_redis and self.redis_client:
            try:
                cached = self.redis_client.get(key)
                if cached:
                    return pickle.loads(cached)
            except Exception as e:
                logger.warning(f"Erreur lecture cache Redis ({key}): {e}")
                # Fallback en mémoire
                return self._get_from_memory(key, default)
        else:
            return self._get_from_memory(key, default)
        
        return default
    
    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = 300,
        ttl: Optional[timedelta] = None
    ) -> bool:
        """
        Met une valeur en cache
        
        Args:
            key: Clé du cache
            value: Valeur à mettre en cache
            ttl_seconds: Durée de vie en secondes (défaut: 300 = 5 min)
            ttl: Durée de vie en timedelta (prioritaire sur ttl_seconds)
            
        Returns:
            True si succès, False sinon
        """
        if ttl:
            ttl_seconds = int(ttl.total_seconds())
        
        if self.use_redis and self.redis_client:
            try:
                serialized = pickle.dumps(value)
                return self.redis_client.setex(key, ttl_seconds, serialized)
            except Exception as e:
                logger.warning(f"Erreur écriture cache Redis ({key}): {e}")
                # Fallback en mémoire
                return self._set_in_memory(key, value, ttl_seconds)
        else:
            return self._set_in_memory(key, value, ttl_seconds)
    
    def delete(self, key: str) -> bool:
        """
        Supprime une clé du cache
        
        Args:
            key: Clé à supprimer
            
        Returns:
            True si succès, False sinon
        """
        if self.use_redis and self.redis_client:
            try:
                return bool(self.redis_client.delete(key))
            except Exception as e:
                logger.warning(f"Erreur suppression cache Redis ({key}): {e}")
        
        # Supprimer aussi du cache mémoire
        if key in self.memory_cache:
            del self.memory_cache[key]
            return True
        
        return False
    
    def delete_pattern(self, pattern: str) -> int:
        """
        Supprime toutes les clés correspondant à un pattern
        
        Args:
            pattern: Pattern Redis (ex: "volume_*")
            
        Returns:
            Nombre de clés supprimées
        """
        count = 0
        
        if self.use_redis and self.redis_client:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    count = self.redis_client.delete(*keys)
            except Exception as e:
                logger.warning(f"Erreur suppression pattern Redis ({pattern}): {e}")
        
        # Nettoyer aussi le cache mémoire
        import time
        current_time = time.time()
        keys_to_delete = [
            k for k in self.memory_cache.keys()
            if self._match_pattern(k, pattern) and self.memory_cache[k][1] < current_time
        ]
        for key in keys_to_delete:
            del self.memory_cache[key]
            count += 1
        
        return count
    
    def exists(self, key: str) -> bool:
        """
        Vérifie si une clé existe dans le cache
        
        Args:
            key: Clé à vérifier
            
        Returns:
            True si la clé existe
        """
        if self.use_redis and self.redis_client:
            try:
                return bool(self.redis_client.exists(key))
            except Exception as e:
                logger.warning(f"Erreur vérification cache Redis ({key}): {e}")
        
        import time
        if key in self.memory_cache:
            _, expiry = self.memory_cache[key]
            if expiry > time.time():
                return True
            else:
                # Expiré, supprimer
                del self.memory_cache[key]
        
        return False
    
    def get_or_set(
        self,
        key: str,
        callable_func,
        ttl_seconds: int = 300,
        ttl: Optional[timedelta] = None
    ) -> Any:
        """
        Récupère une valeur du cache ou l'exécute et la met en cache
        
        Args:
            key: Clé du cache
            callable_func: Fonction à exécuter si la clé n'existe pas
            ttl_seconds: Durée de vie en secondes
            ttl: Durée de vie en timedelta
            
        Returns:
            Valeur en cache ou résultat de callable_func
        """
        cached = self.get(key)
        if cached is not None:
            return cached
        
        # Exécuter la fonction et mettre en cache
        value = callable_func()
        self.set(key, value, ttl_seconds=ttl_seconds, ttl=ttl)
        return value
    
    def clear(self) -> bool:
        """
        Vide tout le cache
        
        Returns:
            True si succès
        """
        if self.use_redis and self.redis_client:
            try:
                self.redis_client.flushdb()
                return True
            except Exception as e:
                logger.warning(f"Erreur vidage cache Redis: {e}")
        
        self.memory_cache.clear()
        return True
    
    def _get_from_memory(self, key: str, default: Any = None) -> Any:
        """Récupère depuis le cache mémoire"""
        import time
        current_time = time.time()
        
        if key in self.memory_cache:
            value, expiry = self.memory_cache[key]
            if expiry > current_time:
                return value
            else:
                # Expiré, supprimer
                del self.memory_cache[key]
        
        return default
    
    def _set_in_memory(self, key: str, value: Any, ttl_seconds: int) -> bool:
        """Met en cache mémoire"""
        import time
        expiry = time.time() + ttl_seconds
        self.memory_cache[key] = (value, expiry)
        return True
    
    def _match_pattern(self, key: str, pattern: str) -> bool:
        """Vérifie si une clé correspond à un pattern simple"""
        import fnmatch
        return fnmatch.fnmatch(key, pattern)
    
    def get_stats(self) -> dict:
        """
        Retourne des statistiques sur le cache
        
        Returns:
            Dictionnaire avec les stats
        """
        stats = {
            "backend": "memory" if not self.use_redis else "redis",
            "memory_cache_size": len(self.memory_cache),
        }
        
        if self.use_redis and self.redis_client:
            try:
                info = self.redis_client.info()
                stats.update({
                    "redis_connected": True,
                    "redis_used_memory": info.get("used_memory_human", "N/A"),
                    "redis_keys": self.redis_client.dbsize(),
                })
            except Exception as e:
                stats["redis_error"] = str(e)
        else:
            stats["redis_connected"] = False
        
        return stats


# Instance globale du service de cache
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """
    Retourne l'instance globale du service de cache (singleton)
    
    Returns:
        Instance de CacheService
    """
    global _cache_service
    
    if _cache_service is None:
        _cache_service = CacheService()
    
    return _cache_service



