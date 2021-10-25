from abc import ABC, abstractmethod
from typing import Dict, List, Mapping, Optional

import requests

from cloudflare.entitie import CloudflareList
from cloudflare.exception import CloudflareInvalidResponse


class HttpServiceBase(ABC):

    @abstractmethod
    def get_common_headers(self) -> Dict[str, str]:
        pass

    def get(self, url: str) -> requests.Response:
        return requests.get(url=url, headers=self.get_common_headers())

    def post(self, url: str, json: Optional[Mapping] = None) -> requests.Response:
        return requests.post(url, json=json, headers=self.get_common_headers())

    def put(self, url: str) -> requests.Response:
        return requests.put(url, headers=self.get_common_headers())

    def delete(self, url: str) -> requests.Response:
        return requests.delete(url, headers=self.get_common_headers())


class CloudflareService(HttpServiceBase):
    email: str
    key: str
    base_url: str
    account_id: int

    def __init__(self, email: str, key: str, base_url: str, account_id: int) -> None:
        self.key = key
        self.email = email
        self.base_url = base_url
        self.account_id = account_id

    def get_common_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.key,
        }

    @classmethod
    def validate_response(cls, response: requests.Response) -> None:
        if response.status_code != 200:
            raise CloudflareInvalidResponse(
                f'Cloudflare server returned unexpected status code: {response.status_code}'
            )

    def get_lists(self) -> List[CloudflareList]:
        response = self.get(self.get_lists_url())
        self.validate_response(response)

        return [CloudflareList(**item) for item in response.json()]

    def get_lists_url(self) -> str:
        return f'{self.base_url}/accounts/{self.account_id}/rules/lists'
