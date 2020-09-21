import os


class ApiClient:

    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key
        self.timeout = timeout


class Service:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client


def main() -> None:
    service = Service(
        api_client=ApiClient(
            api_key=os.getenv('API_KEY'),
            timeout=os.getenv('TIMEOUT'),
        ),
    )
    ...


if __name__ == '__main__':
    main()
