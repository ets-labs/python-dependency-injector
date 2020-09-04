from unittest import mock

from demo import Container


if __name__ == '__main__':
    container = Container()

    with container.api_client.override(mock.Mock()):
        service = container.service()
        assert isinstance(service.api_client, mock.Mock)
