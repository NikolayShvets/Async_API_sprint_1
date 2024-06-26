import backoff
import psycopg2
import psycopg2.extras
from contextlib import closing
from typing import Any
from settings import settings
from logger import logger


class BackoffQueryMixin:
    @backoff.on_exception(backoff.expo, exception=(psycopg2.OperationalError, psycopg2.InterfaceError), logger=logger)
    def _execute_query(self, conn: psycopg2.extensions.connection, query: str) -> list[Any]:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


class UUIDEscapingMixin:
    def escape_uuids(self, uuids: list[str]):
        return ', '.join(map(lambda uuid: f"'{uuid}'", uuids))


@backoff.on_exception(backoff.expo, exception=(psycopg2.OperationalError, psycopg2.InterfaceError), logger=logger)
def get_postges_connection():
    dsl = {
        'dbname': settings['postgres_db_name'],
        'user': settings['postgres_db_user'],
        'password': settings['postgres_db_password'],
        'host': settings['postgres_db_host'],
        'port': settings['postgres_db_port']
    }
    return closing(psycopg2.connect(**dsl, cursor_factory=psycopg2.extras.DictCursor))
