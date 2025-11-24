from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.services.backtest_service import BacktestService


router = APIRouter()


class BacktestResponse(BaseModel):
    """Réponse du backtest"""
    correlation_t1: float
    correlation_t5: float
    accuracy_t1: float
    accuracy_t5: float
    total_periods: int
    period_start: str
    period_end: str
    mean_score: float
    mean_return_t1: float
    mean_return_t5: float


@router.get("/run", summary="Run backtest analysis", response_model=BacktestResponse)
async def run_backtest(
    range: Optional[str] = Query("90d", description="Range: 30d, 90d, 180d, 1y"),
) -> BacktestResponse:
    """
    Exécute un backtest pour mesurer la corrélation entre le score F&G
    et les rendements futurs du marché (T+1, T+5).
    
    - **range**: Période de backtest (30d, 90d, 180d, 1y)
    
    Retourne:
    - correlation_t1: Corrélation score vs rendement à T+1
    - correlation_t5: Corrélation score vs rendement à T+5
    - accuracy_t1: % de prédictions correctes à T+1
    - accuracy_t5: % de prédictions correctes à T+5
    """
    end_date = date.today()
    
    range_map = {
        "30d": 30,
        "90d": 90,
        "180d": 180,
        "1y": 365,
    }
    
    days = range_map.get(range, 90)
    start_date = end_date - timedelta(days=days)
    
    backtest_service = BacktestService()
    result = backtest_service.run_backtest(start_date, end_date)
    
    return BacktestResponse(
        correlation_t1=result.correlation_t1,
        correlation_t5=result.correlation_t5,
        accuracy_t1=result.accuracy_t1,
        accuracy_t5=result.accuracy_t5,
        total_periods=result.total_periods,
        period_start=result.period_start.isoformat(),
        period_end=result.period_end.isoformat(),
        mean_score=result.mean_score,
        mean_return_t1=result.mean_return_t1,
        mean_return_t5=result.mean_return_t5,
    )







