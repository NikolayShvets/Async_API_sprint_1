from fastapi import FastAPI
from async_movies.api.v1.router import api_router
from async_movies.settings.api import api_settings


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
)

app.include_router(
    api_router,
    prefix=api_settings.PREFIX,
)
