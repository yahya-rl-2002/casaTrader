from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class IndexScore(Base):
    __tablename__ = "index_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    as_of = Column(DateTime, nullable=False, index=True)
    score = Column(Float, nullable=False)
    momentum = Column(Float, nullable=True)
    price_strength = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    equity_vs_bonds = Column(Float, nullable=True)
    media_sentiment = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MediaArticle(Base):
    __tablename__ = "media_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    content = Column(String, nullable=True)  # Contenu complet de l'article
    url = Column(String, nullable=False, unique=True)
    source = Column(String, nullable=False)
    image_url = Column(String, nullable=True)  # URL de l'image principale de l'article
    published_at = Column(DateTime, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


# Pydantic schemas for API
class IndexScoreResponse(BaseModel):
    as_of: date
    score: float = Field(..., ge=0.0, le=100.0)
    
    class Config:
        from_attributes = True


class ComponentScoresResponse(BaseModel):
    as_of: date
    momentum: float
    price_strength: float
    volume: float
    volatility: float
    equity_vs_bonds: float
    media_sentiment: float
    
    class Config:
        from_attributes = True


class IndexHistoryResponse(BaseModel):
    data: list[IndexScoreResponse]


class MediaArticleResponse(BaseModel):
    title: str
    summary: str
    url: str
    source: str
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True