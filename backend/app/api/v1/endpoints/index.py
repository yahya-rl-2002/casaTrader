from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.database import get_session
from app.models.schemas import IndexHistoryResponse, IndexScoreResponse, IndexScore

router = APIRouter()


@router.get("/latest", summary="Latest Fear & Greed index value", response_model=IndexScoreResponse)
async def get_latest_index(db: Session = Depends(get_session)) -> IndexScoreResponse:
    latest = db.query(IndexScore).order_by(desc(IndexScore.as_of)).first()
    if latest:
        return IndexScoreResponse(
            as_of=latest.as_of.date(),
            score=latest.score
        )
    else:
        # Return default if no data
        return IndexScoreResponse(
            as_of=date.today(),
            score=50.0
        )


@router.get("/history", summary="Time-series of the Fear & Greed index", response_model=IndexHistoryResponse)
async def get_index_history(
    range: Optional[str] = Query(None, description="Range: 30d, 90d, 180d, 1y, all"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_session)
) -> IndexHistoryResponse:
    """
    Récupère l'historique des scores Fear & Greed.
    
    - **range**: Période prédéfinie (30d, 90d, 180d, 1y, all)
    - **start_date**: Date de début personnalisée
    - **end_date**: Date de fin personnalisée (défaut: aujourd'hui)
    
    Le paramètre `range` a priorité sur start_date/end_date si spécifié.
    """
    query = db.query(IndexScore).order_by(desc(IndexScore.as_of))
    
    # Gérer le paramètre range
    if range:
        if end_date is None:
            end_date = date.today()
        
        range_map = {
            "30d": 30,
            "90d": 90,
            "180d": 180,
            "1y": 365,
        }
        
        if range in range_map:
            start_date = end_date - timedelta(days=range_map[range])
        elif range == "all":
            start_date = None
            end_date = None
    
    if start_date:
        query = query.filter(IndexScore.as_of >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.filter(IndexScore.as_of <= datetime.combine(end_date, datetime.max.time()))
    
    # Limiter à 365 enregistrements max
    scores = query.limit(365).all()
    
    return IndexHistoryResponse(
        data=[
            IndexScoreResponse(
                as_of=score.as_of.date(),
                score=score.score
            )
            for score in scores
        ]
    )

