"""Monitors module."""

import logging
import time
from typing import Dict, Any

from .http import HttpClient


class Monitor:

    def __init__(self, check_every: int) -> None:
        self.check_every = check_every
        self.logger = logging.getLogger(self.__class__.__name__)

    async def check(self) -> None:
        raise NotImplementedError()


class HttpMonitor(Monitor):

    def __init__(
            self,
            http_client: HttpClient,
            options: Dict[str, Any],
    ) -> None:
        self._client = http_client
        self._method = options.pop("method")
        self._url = options.pop("url")
        self._timeout = options.pop("timeout")
        super().__init__(check_every=options.pop("check_every"))

    async def check(self) -> None:
        time_start = time.time()

        response = await self._client.request(
            method=self._method,
            url=self._url,
            timeout=self._timeout,
        )

        time_end = time.time()
        time_took = time_end - time_start

        self.logger.info(
            "Check\n"
            "    %s %s\n"
            "    response code: %s\n"
            "    content length: %s\n"
            "    request took: %s seconds",
            self._method,
            self._url,
            response.status,
            response.content_length,
            round(time_took, 3)
        )
