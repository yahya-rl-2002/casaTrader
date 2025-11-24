"""
Logging structuré amélioré
"""
import logging
import sys
from logging.config import dictConfig
from typing import Any, Dict
import json
from datetime import datetime

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False


def setup_logging(level: str = "INFO", use_json: bool = False) -> None:
    """
    Configure le logging
    
    Args:
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_json: Utiliser le format JSON structuré (pour production)
    """
    if STRUCTLOG_AVAILABLE and use_json:
        # Logging structuré JSON
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        # Logging standard
        format_string = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        
        dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "standard": {
                        "format": format_string,
                    },
                    "json": {
                        "()": "app.core.logging.JSONFormatter",
                        "format": format_string,
                    },
                },
                "handlers": {
                    "default": {
                        "level": level,
                        "formatter": "json" if use_json else "standard",
                        "class": "logging.StreamHandler",
                        "stream": sys.stdout,
                    },
                },
                "root": {
                    "handlers": ["default"],
                    "level": level,
                },
            }
        )


class JSONFormatter(logging.Formatter):
    """Formatter JSON pour logging structuré"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formate un log en JSON"""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Ajouter les champs supplémentaires
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Ajouter l'exception si présente
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Ajouter les champs standards
        if record.pathname:
            log_data["pathname"] = record.pathname
        if record.lineno:
            log_data["lineno"] = record.lineno
        if record.funcName:
            log_data["function"] = record.funcName
        
        return json.dumps(log_data)


def get_logger(name: str) -> logging.Logger:
    """
    Retourne un logger
    
    Args:
        name: Nom du logger (généralement __name__)
    
    Returns:
        Logger configuré
    """
    if STRUCTLOG_AVAILABLE:
        return structlog.get_logger(name)
    else:
        return logging.getLogger(name)


def get_structured_logger(name: str):
    """
    Retourne un logger structuré (si structlog est disponible)
    
    Args:
        name: Nom du logger
    
    Returns:
        Logger structuré ou logger standard
    """
    if STRUCTLOG_AVAILABLE:
        return structlog.get_logger(name)
    else:
        logger = logging.getLogger(name)
        # Wrapper pour simuler l'interface structlog
        class StructuredLogger:
            def __init__(self, logger):
                self._logger = logger
            
            def bind(self, **kwargs):
                """Bind des champs supplémentaires"""
                self._extra = kwargs
                return self
            
            def _log(self, level, msg, *args, **kwargs):
                """Log avec les champs supplémentaires"""
                if hasattr(self, '_extra'):
                    kwargs.update(self._extra)
                getattr(self._logger, level)(msg, *args, extra=kwargs)
            
            def debug(self, msg, *args, **kwargs):
                self._log('debug', msg, *args, **kwargs)
            
            def info(self, msg, *args, **kwargs):
                self._log('info', msg, *args, **kwargs)
            
            def warning(self, msg, *args, **kwargs):
                self._log('warning', msg, *args, **kwargs)
            
            def error(self, msg, *args, **kwargs):
                self._log('error', msg, *args, **kwargs)
            
            def critical(self, msg, *args, **kwargs):
                self._log('critical', msg, *args, **kwargs)
        
        return StructuredLogger(logger)
