import os


class ApiClient:

    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.timeout = os.getenv('TIMEOUT')


class Service:

    def __init__(self):
        self.api_client = ApiClient()


def main() -> None:
    service = Service()
    ...


if __name__ == '__main__':
    main()
