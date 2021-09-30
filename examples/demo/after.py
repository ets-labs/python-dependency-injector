import os


class ApiClient:

    def __init__(self, api_key: str, timeout: int):
        self.api_key = api_key  # <-- dependency is injected
        self.timeout = timeout  # <-- dependency is injected


class Service:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client  # <-- dependency is injected


def main(service: Service):  # <-- dependency is injected
    ...


if __name__ == "__main__":
    main(
        service=Service(
            api_client=ApiClient(
                api_key=os.getenv("API_KEY"),
                timeout=os.getenv("TIMEOUT"),
            ),
        ),
    )
