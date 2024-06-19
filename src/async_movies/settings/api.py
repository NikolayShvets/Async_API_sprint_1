from async_movies.settings.base import BaseSettings


class APISettings(BaseSettings):
    TITLE: str = "async-movies"
    PREFIX: str = "/async-movies/api"
    OPENAPI_URL: str = "/async-movies/api/v1/public/openapi.json"
    DOCS_URL: str = "/async-movies/api/v1/public/docs"
    REDOC_URL: str = "/async-movies/api/v1/public/redoc"

    LOG_QUERIES: bool = False


api_settings = APISettings()
