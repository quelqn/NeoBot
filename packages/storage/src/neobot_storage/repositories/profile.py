"""SqlAlchemy profile repository (users + groups)."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.sqlite import insert

from neobot_storage.models import UserData, GroupData


class SqlAlchemyProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_user(self, user_id: str, **fields) -> None:
        stmt = insert(UserData).values(user_id=user_id, **fields)
        stmt = stmt.on_conflict_do_update(index_elements=["user_id"], set_=fields)
        await self._session.execute(stmt)

    async def upsert_group(self, group_id: str, **fields) -> None:
        stmt = insert(GroupData).values(group_id=group_id, **fields)
        stmt = stmt.on_conflict_do_update(index_elements=["group_id"], set_=fields)
        await self._session.execute(stmt)

    async def user_exists(self, user_id: str) -> bool:
        from sqlalchemy import select
        stmt = select(UserData.user_id).where(UserData.user_id == user_id).limit(1)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def group_exists(self, group_id: str) -> bool:
        from sqlalchemy import select
        stmt = select(GroupData.group_id).where(GroupData.group_id == group_id).limit(1)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
