from settings.base import BaseSettings


class ETLProcessSettings(BaseSettings):
    ETL_PROCESS_DELAY: int = 60 * 60  # in seconds
    ETL_PROCESS_BATCH_SIZE: int = 1000


etl_process_config = ETLProcessSettings()
