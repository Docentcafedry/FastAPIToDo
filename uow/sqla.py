from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseUnitOfWork


class SQLAUnitOfWork(BaseUnitOfWork):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def rollback(self) -> None:
        print("Rolling back transaction")
        await self.db.rollback()

    async def commit(self) -> None:
        print("Commiting transaction")
        await self.db.commit()
