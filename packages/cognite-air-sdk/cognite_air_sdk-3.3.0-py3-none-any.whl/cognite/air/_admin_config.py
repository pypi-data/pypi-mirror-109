import json

import requests

from cognite.client import CogniteClient


class AdminAPI:
    _ENDPOINT = "/"

    def __init__(self, client: CogniteClient, project: str, staging: bool = True):
        self.client = client
        self.project = project
        self.staging = staging
        self.headers = {"api-key": self.client.config.api_key, "Content-Type": "application/json"}

    @property
    def _api_url(self) -> str:
        url = f"https://air-api.{'staging.' if self.staging else ''}cognite.ai/project/" + self.project
        return url

    def _post(self, payload):
        r = requests.post(self._api_url + self._ENDPOINT, data=json.dumps(payload), headers=self.headers)
        if r.status_code > 200:
            raise ValueError(r.content)

    def _get(self):
        pass
