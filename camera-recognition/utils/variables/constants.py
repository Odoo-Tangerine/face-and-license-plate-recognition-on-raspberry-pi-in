from typing import Final
from dotenv import load_dotenv
from os import environ, path
from enum import Enum

BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, '.env'))


class Const(Enum):
    DB_HOST: Final[str] = environ.get('DB_HOST')
    DB_NAME: Final[str] = environ.get('DB_NAME')
    DB_USER: Final[str] = environ.get('DB_USER')
    DB_PW: Final[str] = environ.get('DB_PW')
    DB_PORT: Final[str] = environ.get('DB_PORT')

    ODOO_SERVER_DOMAIN: Final[str] = environ.get('ODOO_SERVER_DOMAIN')