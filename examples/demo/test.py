from unittest import mock

import demo


if __name__ == '__main__':
    container = demo.Container()
    container.wire(modules=[demo])

    with container.api_client.override(mock.Mock()):
        demo.main()
