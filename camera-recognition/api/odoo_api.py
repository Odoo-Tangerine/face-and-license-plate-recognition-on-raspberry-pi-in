import aiohttp
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional
from ..utils.variables.constants import Const


_logger = logging.getLogger(__name__)


@dataclass
class OdooAPI:
    odoo_url: str = Const.ODOO_SERVER_DOMAIN.value

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
        if response and response.get('status') == 200:
            return response.get('data')
        return None

    async def authenticate_into_parking(self, license_plate: str) -> Optional[Dict[str, Dict[str, Any]]]:
        try:
            url = f'{self.odoo_url}/odoo-api/raspberry/authenticate/in_parking'
            response = await self.make_request(url=url, method='POST', data={'license_plate': license_plate})
            return self.check_response(response)
        except Exception as e:
            _logger.exception(e)