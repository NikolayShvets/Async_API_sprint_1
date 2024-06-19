from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from async_movies.settings.postgresql import postgresql_settings
from async_movies.settings.api import api_settings


async_engine = create_async_engine(
    postgresql_settings.DSN,
    echo=api_settings.LOG_QUERIES,
)

async_session_factory = async_sessionmaker(
    engine=async_engine,
    expire_on_commit=False,
)
