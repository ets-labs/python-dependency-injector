"""Monitors module."""

import logging
from typing import Dict, Any

from .http import HttpClient


class Monitor:

    def __init__(self, check_every: int) -> None:
        self.check_every = check_every
        self.logger = logging.getLogger(self.full_name)

    @property
    def full_name(self) -> str:
        raise NotImplementedError()

    async def check(self) -> None:
        raise NotImplementedError()


class HttpMonitor(Monitor):

    def __init__(
            self,
            http_client: HttpClient,
            options: Dict[str, Any],
    ) -> None:
        self._client = http_client
        self._method = options.pop('method')
        self._url = options.pop('url')
        self._expected_codes = options.pop('expected_codes')
        super().__init__(check_every=options.pop('check_every'))

    @property
    def full_name(self) -> str:
        return '{0}.{1}(url="{2}")'.format(__name__, self.__class__.__name__, self._url)

    async def check(self) -> None:
        response = await self._client.request(method=self._method, url=self._url)
        self.logger.info('Return response code: %s', response.status)
