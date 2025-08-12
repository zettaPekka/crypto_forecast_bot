from fastapi import APIRouter, Query, Depends

from app.dependencies import get_trader_data_service
from database.services.trader_data_service import TraderDataService


router = APIRouter()


@router.get('/reg/')
async def reg(
    trader_id: int = Query(),
    trader_data_service: TraderDataService = Depends(get_trader_data_service)
):
    await trader_data_service.create(trader_id)


@router.get('/dep/')
async def dep(
    trader_id: int = Query(),
    sumdep: float =  Query(),
    trader_data_service: TraderDataService = Depends(get_trader_data_service)
):
    await trader_data_service.dep(sumdep, trader_id)