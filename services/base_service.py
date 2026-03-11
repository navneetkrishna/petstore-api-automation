import requests
import config

class BaseService:

    def __init__(self):
        self.base_url = config.BASE_URL
        self.session = requests.Session()
        self.headers = config.HEADERS
        self.timeout = config.TIMEOUT
        self.session.headers.update(self.headers)


    def get(self, endpoint, params=None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=self.timeout)


    def post(self, endpoint, data=None, files=None, json=None, params=None):
        return self.session.post(f"{self.base_url}{endpoint}")