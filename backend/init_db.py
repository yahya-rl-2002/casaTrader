#!/usr/bin/env python3
"""
Initialize the database with sample data
"""
import asyncio
from datetime import date, datetime, timedelta
from random import uniform

from app.models.database import engine, metadata
from app.models.schemas import IndexScore, MediaArticle, Base


def create_sample_data():
    """Create sample data for development"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create sample index scores for the last 30 days
        for i in range(30):
            as_of = datetime.now() - timedelta(days=i)
            score = uniform(20, 80)  # Random score between 20-80
            
            index_score = IndexScore(
                as_of=as_of,
                score=score,
                momentum=uniform(0, 100),
                price_strength=uniform(0, 100),
                volume=uniform(0, 100),
                volatility=uniform(0, 100),
                equity_vs_bonds=uniform(0, 100),
                media_sentiment=uniform(0, 100)
            )
            db.add(index_score)
        
        # Create sample media articles
        sample_articles = [
            {
                "title": "Perspectives positives pour le MASI",
                "summary": "Les analystes prévoient une reprise progressive des volumes sur le marché marocain dans les prochains mois.",
                "url": "https://example.com/article-1",
                "source": "Medias24",
                "published_at": datetime.now() - timedelta(hours=2),
                "sentiment_score": 0.7
            },
            {
                "title": "Croissance soutenue des investissements",
                "summary": "Le marché marocain continue d'attirer les investisseurs étrangers avec des performances remarquables.",
                "url": "https://example.com/article-2",
                "source": "L'Économiste",
                "published_at": datetime.now() - timedelta(hours=5),
                "sentiment_score": 0.8
            },
            {
                "title": "Volatilité accrue sur les marchés",
                "summary": "Les tensions géopolitiques créent une incertitude sur les marchés financiers marocains.",
                "url": "https://example.com/article-3",
                "source": "BourseNews",
                "published_at": datetime.now() - timedelta(hours=8),
                "sentiment_score": -0.3
            }
        ]
        
        for article_data in sample_articles:
            article = MediaArticle(**article_data)
            db.add(article)
        
        db.commit()
        print("✅ Sample data created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()







