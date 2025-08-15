from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from database.models import Statistics


class StatRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def add(self, date: str, profit: int, loss: int, break_even: int):
        trader_data = Statistics(date=date, profit=profit, loss=loss, break_even=break_even)
        self.session.add(trader_data)
    
    async def get_last_week(self):
        days = await self.session.execute(select(Statistics).order_by(desc(Statistics.id)).limit(7))
        days = days.scalars().all()
        return days
    
    async def get_last_day(self):
        return await self.session.scalar(select(Statistics).order_by(desc(Statistics.id)).limit(1))