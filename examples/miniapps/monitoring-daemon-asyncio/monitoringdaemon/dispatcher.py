"""Dispatcher module."""

import asyncio
import logging
import signal
import time
from typing import List

from .monitors import Monitor


logger = logging.getLogger(__name__)


class Dispatcher:

    def __init__(self, monitors: List[Monitor]) -> None:
        self._monitors = monitors
        self._monitor_tasks: List[asyncio.Task] = []
        self._stopping = False

    def run(self) -> None:
        asyncio.run(self.start())

    async def start(self) -> None:
        logger.info('Dispatcher is starting up')

        for monitor in self._monitors:
            self._monitor_tasks.append(
                asyncio.create_task(self._run_monitor(monitor)),
            )
            logger.info(
                'Monitoring task has been started %s',
                monitor.full_name,
            )

        asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, self.stop)
        asyncio.get_event_loop().add_signal_handler(signal.SIGINT, self.stop)

        await asyncio.gather(*self._monitor_tasks, return_exceptions=True)

        self.stop()

    def stop(self) -> None:
        if self._stopping:
            return

        self._stopping = True

        logger.info('Dispatcher is shutting down')
        for task, monitor in zip(self._monitor_tasks, self._monitors):
            task.cancel()
            logger.info('Monitoring task has been stopped %s', monitor.full_name)
        logger.info('Dispatcher shutting down finished successfully')

    @staticmethod
    async def _run_monitor(monitor: Monitor) -> None:
        def _until_next(last: float) -> float:
            time_took = time.time() - last
            return monitor.check_every - time_took

        while True:
            time_start = time.time()

            try:
                await monitor.check()
            except asyncio.CancelledError:
                break
            except Exception:
                monitor.logger.exception('Error running monitoring check')

            await asyncio.sleep(_until_next(last=time_start))
