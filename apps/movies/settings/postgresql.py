from pydantic import PostgresDsn, SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from settings.base import BaseSettings


class PostgreSQLSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    DSN: str | None = None

    @field_validator("DSN", mode="before")
    def assemble_db_url(cls, value: str | None, info: FieldValidationInfo) -> str:
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"].get_secret_value(),
            host=info.data["POSTGRES_HOST"],
            port=info.data["POSTGRES_PORT"],
            path=info.data["POSTGRES_DB"],
        ).unicode_string()


postgresql_settings = PostgreSQLSettings()
