import requests
import jmespath


class DatasourceEngine:
    def __init__(self, datasource):
        self.datasource = datasource

    def fetch(self, params: dict = None) -> dict:
        headers = {}
        if getattr(self.datasource, "auth_token", None):
            headers["Authorization"] = f"Bearer {self.datasource.auth_token}"
        resp = requests.get(self.datasource.api_endpoint, headers=headers, params=params or {}, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def extract_value(self, data: dict, key: str):
        if not key:
            return data
        return jmespath.search(key, data)
