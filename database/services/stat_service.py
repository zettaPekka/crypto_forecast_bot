from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.stat_repo import StatRepo


class StatService:
    def __init__(self, session: AsyncSession, stat_repo: StatRepo):
        self.session = session
        self.stat_repo = stat_repo
    
    async def add(self, date: str, profit: int, loss: int, break_even: int):
        self.stat_repo.add(date, profit, loss, break_even)
        await self.session.commit()
    
    async def get_last_week(self):
        return await self.stat_repo.get_last_week()
    
    async def get_last_day(self):
        date = await self.stat_repo.get_last_day()
        return date