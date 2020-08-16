import os


class ApiClient:

    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key
        self.timeout = timeout


class Service:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client


if __name__ == '__main__':
    service = Service(ApiClient(os.getenv('API_KEY'), os.getenv('TIMEOUT')))
