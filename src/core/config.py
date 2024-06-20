import os
from logging import config as logging_config
from dotenv import load_dotenv

from core.logger import LOGGING

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(f'{BASE_DIR}/.env')

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'http://localhost')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

# Настройки PostgreSQL
POSTGRES_DB_USER = os.getenv('POSTGRES_DB_USER', 'app')
POSTGRES_DB_PASSWORD = os.getenv('POSTGRES_DB_PASSWORD', '123qwe')
POSTGRES_DB_HOST = os.getenv('POSTGRES_DB_HOST', 'localhost')
POSTGRES_DB_PORT = int(os.getenv('POSTGRES_DB_PORT', 5432))
POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME', 'movies_database')
POSTGRES_DB_POOL_RECYCLE = int(os.getenv('POSTGRES_DB_POOL_RECYCLE', 60))
POSTGRES_DB_MAX_CONNECTIONS = int(os.getenv('POSTGRES_DB_MAX_CONNECTIONS', 10))
POSTGRES_DB_ECHO = bool(os.getenv('POSTGRES_DB_ECHO', False))
