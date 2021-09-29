import os


class ApiClient:

    def __init__(self):
        self.api_key = os.getenv("API_KEY")  # <-- dependency
        self.timeout = os.getenv("TIMEOUT")  # <-- dependency


class Service:

    def __init__(self):
        self.api_client = ApiClient()  # <-- dependency


def main() -> None:
    service = Service()  # <-- dependency
    ...


if __name__ == "__main__":
    main()
