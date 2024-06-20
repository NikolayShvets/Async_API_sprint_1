from typing import Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from pydantic import PostgresDsn

from core.config import (
    POSTGRES_DB_USER, POSTGRES_DB_PASSWORD, POSTGRES_DB_HOST, POSTGRES_DB_PORT, POSTGRES_DB_NAME,
    POSTGRES_DB_POOL_RECYCLE, POSTGRES_DB_MAX_CONNECTIONS, POSTGRES_DB_ECHO
)

postgres_db_engine: Optional[AsyncEngine] = None
async_session: Optional[async_sessionmaker[AsyncSession]] = None


def setup_postgres_connection():
    global postgres_db_engine, async_session

    url = PostgresDsn.build(
        scheme='postgresql+asyncpg',
        username=POSTGRES_DB_USER,
        password=POSTGRES_DB_PASSWORD,
        host=POSTGRES_DB_HOST,
        port=POSTGRES_DB_PORT,
        path=POSTGRES_DB_NAME,
    ).unicode_string()

    postgres_db_engine = create_async_engine(
        url=url,
        pool_recycle=POSTGRES_DB_POOL_RECYCLE,
        pool_size=POSTGRES_DB_MAX_CONNECTIONS,
        echo=POSTGRES_DB_ECHO,
    )

    async_session = async_sessionmaker(
        bind=postgres_db_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )


async def close_postgres_connection():
    await postgres_db_engine.dispose()


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
