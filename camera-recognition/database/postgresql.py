import logging
import psycopg2
from psycopg2.errors import ConnectionException
from dataclasses import dataclass
from ..utils.variables.constants import Const


_logger = logging.getLogger(__name__)


@dataclass
class Postgres:
    host: str = Const.DB_HOST.value
    database: str = Const.DB_NAME.value
    user: str = Const.DB_USER.value
    password: str = Const.DB_PW.value
    port: str = Const.DB_PORT.value

    def get_connection(self):
        try:
            return psycopg2.connect(
                 host=self.host,
                 database=self.database,
                 user=self.user,
                 password=self.password,
                 port=self.port
           )
        except ConnectionException as e:
           _logger.exception(e)

    def execute_query(self, query: str):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
                    return cursor.fetchall()
        except Exception as e:
            conn.rollback()
            _logger.exception(e)