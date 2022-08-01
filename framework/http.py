from dataclasses import dataclass, field

import requests
from requests import Response as RequestsResponse

from utils.data_util import DataUtil


@dataclass
class Request:
    method: str = None
    host: str = None
    path: str = None
    query: dict = None
    headers: dict = field(default_factory=dict)
    type: str = 'json'
    data: dict = None

    def send(self):
        env = DataUtil.load_yaml('data/env.yaml')
        self.host = env[env['default']]

        

        requests_response = requests.request(
            method=self.method,
            url=self.host + self.path,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            timeout=None,
            proxies=None,
            verify=None,
            json=None,
        )

        r = Response(requests_response)
        return r


@dataclass
class Response:

    def __init__(self, requests_response):
        self.r: RequestsResponse = requests_response

    def json(self):
        return self.r.json()

    @property
    def text(self):
        return self.r.text

    @property
    def status_code(self):
        return self.r.status_code
