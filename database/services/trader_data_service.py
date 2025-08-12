from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import TraderData
from database.repositories.trader_data_repo import TraderDataRepo


class TraderDataService:
    def __init__(self, session: AsyncSession, trader_data_repo: TraderDataRepo):
        self.session = session
        self.trader_data_repo = trader_data_repo
    
    async def create(self, trader_id: int):
        self.trader_data_repo.add(trader_id)
        await self.session.commit()
    
    async def get(self, trader_id: int):
        return await self.trader_data_repo.get(trader_id)

    async def get_by_tg_id(self, tg_id: int):
        return await self.trader_data_repo.get_by_tg_id(tg_id)
    
    async def dep(self, sumdep: float, trader_id: int):
        trader_data = await self.get(trader_id)
        if trader_data:
            await self.trader_data_repo.dep(sumdep, trader_id)
            await self.session.commit()

    async def check_trader_id(self, trader_id: int, tg_id: int):
        res = await self.trader_data_repo.check_trader_id(trader_id)
        if not res:
            return False
        await self.trader_data_repo.link_ids(trader_id, tg_id)
        await self.session.commit()
        return True