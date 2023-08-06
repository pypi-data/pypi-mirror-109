import posixpath
from enum import Enum
from types import Union
from urllib.error import HTTPError
from urllib.parse import urljoin

from requests import Session

from auto_ria_client.constants import AUTO_RIA_BASE_URL
from auto_ria_client.enums import TransportCategory
from auto_ria_client.errors import AutoRiaHTTPError


class AutoClient:

    def __init__(self, api_key: str):
        self.session = Session()
        self.api_key = api_key

    def request_api(self, path: str, params: dict = None) -> dict:
        url = urljoin(AUTO_RIA_BASE_URL, posixpath.join('auto', path))
        try:
            response = self.session.get(url, params={
                "api_key": self.api_key,
                **(params or {})
            })
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            raise AutoRiaHTTPError(response=e.response) from e

    def get_transport_categories(self) -> dict:
        return self.request_api("categories")

    def get_fuel_types(self):
        return self.request_api(f'type')

    def get_body_types(self, transport_category_id: int) -> dict:
        return self.request_api(f'categories/{transport_category_id}/bodystyles')

    def get_brands_types(self, transport_category_id: int) -> dict:
        return self.request_api(f'categories/{transport_category_id}/marks')

    def get_brand_models(self, transport_category_id: int, brand_id: int) -> dict:
        return self.request_api(f'categories/{transport_category_id}/marks/{brand_id}/models')

    def get_states(self) -> dict:
        return self.request_api(f'states')

    def get_cities(self, state_id: int):
        return self.request_api(f'states/{state_id}/cities')

    def get_driver_types(self, transport_category_id: int) -> dict:
        return self.request_api(f'categories/{transport_category_id}/driverTypes')

    def get_gearbox_types(self, transport_category_id: int) -> dict:
        return self.request_api(f'categories/{transport_category_id}/gearboxes')

