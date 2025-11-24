from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.database import get_session
from app.models.schemas import ComponentScoresResponse, IndexScore

router = APIRouter()


@router.get("/latest", summary="Latest component breakdown", response_model=ComponentScoresResponse)
async def get_latest_components(db: Session = Depends(get_session)) -> ComponentScoresResponse:
    latest = db.query(IndexScore).order_by(desc(IndexScore.as_of)).first()
    if latest:
        return ComponentScoresResponse(
            as_of=latest.as_of.date(),
            momentum=latest.momentum or 50.0,
            price_strength=latest.price_strength or 50.0,
            volume=latest.volume or 50.0,
            volatility=latest.volatility or 50.0,
            equity_vs_bonds=latest.equity_vs_bonds or 50.0,
            media_sentiment=latest.media_sentiment or 50.0,
        )
    else:
        # Return default values if no data
        return ComponentScoresResponse(
            as_of=date.today(),
            momentum=50.0,
            price_strength=50.0,
            volume=50.0,
            volatility=50.0,
            equity_vs_bonds=50.0,
            media_sentiment=50.0,
        )

