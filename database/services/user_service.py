from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.repositories.user_repo import UserRepo


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
