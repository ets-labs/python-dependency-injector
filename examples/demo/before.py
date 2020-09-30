import os


class ApiClient:

    def __init__(self):
        self.api_key = os.getenv('API_KEY')  # <-- the dependency
        self.timeout = os.getenv('TIMEOUT')  # <-- the dependency


class Service:

    def __init__(self):
        self.api_client = ApiClient()  # <-- the dependency


def main() -> None:
    service = Service()  # <-- the dependency
    ...


if __name__ == '__main__':
    main()
