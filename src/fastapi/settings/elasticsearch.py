from pydantic import HttpUrl, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from settings.base import BaseSettings


class ElasticsearchSettings(BaseSettings):
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    ELASTICSEARCH_URL: str | None = None

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


elasticsearch_settings = ElasticsearchSettings()
