from contextlib import asynccontextmanager

import asyncpg
from api.v1.router import api_router
from db import elasticsearch, postgresql, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import StrictRedis
from settings.api import api_settings
from settings.elasticsearch import elasticsearch_settings
from settings.postgresql import postgresql_settings
from settings.redis import redis_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgresql.session = await asyncpg.connect(postgresql_settings.DSN)
    redis.redis = StrictRedis.from_url(redis_settings.REDIS_URL)
    elasticsearch.es = AsyncElasticsearch(elasticsearch_settings.ELASTICSEARCH_URL)
    try:
        yield
    finally:
        await postgresql.session.close()
        await redis.redis.close()
        await elasticsearch.es.close()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


app.include_router(api_router)
