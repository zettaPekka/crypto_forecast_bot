from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database.models import TraderData


class TraderDataRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def add(self, trader_id: int):
        trader_data = TraderData(trader_id=trader_id)
        self.session.add(trader_data)
    
    async def get(self, trader_id: int):
        return await self.session.get(TraderData, trader_id)

    async def get_by_tg_id(self, tg_id: int):
        return await self.session.scalar(select(TraderData).where(TraderData.tg_id == tg_id))

    async def dep(self, sumdep: float, trader_id: int):
        trader_data = await self.get(trader_id)
        trader_data.balance += sumdep
    
    async def check_trader_id(self, trader_id) -> None | TraderData:
        trader_data = await self.session.scalar(select(TraderData).where(
            and_(
                TraderData.trader_id == trader_id,
                TraderData.tg_id == None
            )
        ))
        return trader_data

    async def link_ids(self, trader_id: int, tg_id: int):
        trader_data = await self.get(trader_id)
        trader_data.tg_id = tg_id
    
    async def get_reg_traders(self):
        traders = await self.session.execute(select(TraderData).where(TraderData.tg_id))
        traders = traders.scalars().all()
        return traders
    
    async def get_active_traders(self):
        traders = await self.session.execute(select(TraderData).where(TraderData.balance > 0))
        traders = traders.scalars().all()
        return traders