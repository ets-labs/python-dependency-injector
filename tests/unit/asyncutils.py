"""Test utils."""

import asyncio
import contextlib
import sys
import gc
import unittest


def run(main):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(main)


def setup_test_loop(
        loop_factory=asyncio.new_event_loop
) -> asyncio.AbstractEventLoop:
    loop = loop_factory()
    try:
        module = loop.__class__.__module__
        skip_watcher = 'uvloop' in module
    except AttributeError:  # pragma: no cover
        # Just in case
        skip_watcher = True
    asyncio.set_event_loop(loop)
    if sys.platform != 'win32' and not skip_watcher:
        policy = asyncio.get_event_loop_policy()
        watcher = asyncio.SafeChildWatcher()  # type: ignore
        watcher.attach_loop(loop)
        with contextlib.suppress(NotImplementedError):
            policy.set_child_watcher(watcher)
    return loop


def teardown_test_loop(loop: asyncio.AbstractEventLoop, fast: bool = False) -> None:
    closed = loop.is_closed()
    if not closed:
        loop.call_soon(loop.stop)
        loop.run_forever()
        loop.close()

    if not fast:
        gc.collect()

    asyncio.set_event_loop(None)


class AsyncTestCase(unittest.TestCase):

    def setUp(self):
        self.loop = setup_test_loop()

    def tearDown(self):
        teardown_test_loop(self.loop)

    def _run(self, f):
        return self.loop.run_until_complete(f)
