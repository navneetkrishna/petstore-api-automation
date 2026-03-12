import requests
import config

class BaseService:

    def __init__(self):
        self.base_url = config.BASE_URL
        self.session = requests.Session()
        self.headers = config.HEADERS
        self.timeout = config.TIMEOUT
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_key": config.API_KEY,
        })


    def get(self, endpoint, params=None):
        return self.session.get(
            f"{self.base_url}{endpoint}",
            params=params,
            timeout=self.timeout
        )

    def post(self, endpoint, payload):
        return self.session.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            timeout=self.timeout
        )

    def put(self, endpoint, payload):
        return self.session.put(
            f"{self.base_url}{endpoint}",
            json=payload,
            timeout=self.timeout
        )

    def patch(self, endpoint, payload):
        return self.session.patch(
            f"{self.base_url}{endpoint}",
            json=payload,
            timeout=self.timeout
        )

    def delete(self, endpoint):
        return self.session.delete(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout
        )