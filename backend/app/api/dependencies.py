"""Shared FastAPI dependencies."""

from collections.abc import Generator
from typing import Generator as TypingGenerator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.models.database import get_session as _get_session


# Database session dependency for FastAPI
def get_db() -> Generator[Session, None, None]:
    """
    Dependency pour obtenir une session de base de données.
    Ferme automatiquement la session après utilisation.
    """
    db = _get_session()
    try:
        yield db
    finally:
        db.close()


# Example dependency usage point for routers
def get_settings() -> dict:
    from app.core.config import settings

    return settings


SettingsDependency = Depends(get_settings)



