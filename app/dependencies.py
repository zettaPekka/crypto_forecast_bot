from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from database.services.trader_data_service import TraderDataService
from database.repositories.trader_data_repo import TraderDataRepo


async def get_trader_data_service():
    async with get_session() as session:
        trader_data_service = TraderDataService(session, TraderDataRepo(session))
        return trader_data_service