from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


class DatabaseHelper:
    def __init__(self):
        self.async_engine = create_async_engine(
            url=settings.db_url,
            echo=settings.db_echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.get_scoped_session()
        async with session() as sess:
            yield sess
            await session.remove()


db_helper = DatabaseHelper()
