from fastapi import APIRouter

router = APIRouter()


@router.get("/weights", summary="Weighting schema for index components")
async def get_weights() -> dict[str, float]:
    return {
        "momentum": 0.20,
        "price_strength": 0.15,
        "volume": 0.15,
        "volatility": 0.20,
        "equity_vs_bonds": 0.15,
        "media_sentiment": 0.15,
    }


@router.get("/components", summary="List of index components")
async def get_component_list() -> dict[str, list[str]]:
    return {"components": list(get_weights().keys())}

