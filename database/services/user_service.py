from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.repositories.user_repo import UserRepo

from typing import Literal


class UserService:
    def __init__(self, session: AsyncSession, user_repo: UserRepo):
        self.session = session
        self.user_repo = user_repo
    
    async def create_if_not_exists(self, tg_id: int):
        user = await self.get(tg_id)
        if not user:
            self.user_repo.add(tg_id)
            await self.session.commit()
    
    async def get(self, tg_id: int) -> User | None:
        return await self.user_repo.get(tg_id)
    
    async def change_otc(self, tg_id) -> bool:
        user = await self.get(tg_id)
        user.otc = False if user.otc else True
        await self.session.commit()
        return user.otc

    async def get_all_users(self):
        return await self.user_repo.get_all_users()
