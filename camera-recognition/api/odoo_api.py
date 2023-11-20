import aiohttp
import logging
from dotenv import load_dotenv
from os import environ, path
from dataclasses import dataclass
from typing import Dict, Any, Optional


BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, '.env'))


_logger = logging.getLogger(__name__)


@dataclass
class OdooAPI:
    odoo_url: str = environ.get('ODOO_SERVER_DOMAIN')

    @staticmethod
    async def make_request(url: str, method: str, data: Optional[Dict[str, Any]] = None, **kwargs):
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(url=url, **kwargs) as response:
                        return await response.json()
                else:
                    async with session.post(url=url, data=data, **kwargs) as response:
                        return await response.json()
        except Exception as e:
            _logger.exception(e)

    @staticmethod
    def check_response(response):
        if response:
            if response.get('status') and response.get('status') == 200:
                return response.get('data', 'Success')
        return None

    async def authenticate_into_parking(self, license_plate: str) -> Optional[Dict[str, Dict[str, Any]]]:
        try:
            url = f'{self.odoo_url}/odoo-api/raspberry/authenticate/in_parking?license_plate={license_plate}'
            response = await self.make_request(url=url, method='POST')
            return self.check_response(response)
        except Exception as e:
            _logger.exception(e)

    async def post_history_got_inside_parking(self, user_id, user_name):
        try:
            url = f'{self.odoo_url}/odoo-api/raspberry/authenticate/history?user_id={user_id}?user_name={user_name}?type=in'
            response = await self.make_request(url=url, method='POST')
            return self.check_response(response)
        except Exception as e:
            _logger.exception(e)
