import asyncpg

session: asyncpg.Connection | None = None


async def get_session() -> asyncpg.Connection:
    return session
