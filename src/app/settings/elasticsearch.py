from pathlib import Path

from pydantic import HttpUrl, RedisDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from settings.base import ROOT_DIR, BaseSettings


class ElasticsearchSettings(BaseSettings):
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    ELASTICSEARCH_URL: str | None = None

    ELASTICSEARCH_INDEX_PATH: Path

    @field_validator("ELASTICSEARCH_URL", mode="before")
    def assemble_elasticsearch_url(
        cls, v: str | None, info: FieldValidationInfo
    ) -> str:
        if isinstance(v, str):
            return v

        scheme = "http"
        host = info.data["ELASTICSEARCH_HOST"]
        port = info.data["ELASTICSEARCH_PORT"]

        url = f"{scheme}://{host}:{port}"
        return HttpUrl(url).unicode_string()

    @field_validator("ELASTICSEARCH_INDEX_PATH", mode="before")
    def assemble_elasticsearch_index_path(cls, v: str) -> Path:
        return ROOT_DIR.joinpath(v)


elasticsearch_settings = ElasticsearchSettings()
