import os
from unittest import TestCase

from core.api.settings import _Config
from core.utils.Executor import Executor


class TestExecutor(TestCase):
    def test_logged_call(self):
        if os.path.exists(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
        ):
            os.remove(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
            )

        e1 = Executor(
            _Config.ROOT_DIR,
            logfile='log.tmp'
        )

        e1.logged_call('echo THOR')

        with open(os.path.join(_Config.ROOT_DIR, 'log.tmp'), 'r') as f:
            self.assertEqual(
                f.readline().strip('\n'),
                'THOR'
            )

        os.remove(
            os.path.join(_Config.ROOT_DIR, 'log.tmp')
        )

    def test_is_running(self):
        if os.path.exists(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
        ):
            os.remove(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
            )

        e2 = Executor(
            _Config.ROOT_DIR,
            logfile='log.tmp'
        )

        e2.call('ls')

        self.assertFalse(e2.is_running())

        os.remove(
            os.path.join(_Config.ROOT_DIR, 'log.tmp')
        )

    def test_terminate(self):
        if os.path.exists(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
        ):
            os.remove(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
            )

        e3 = Executor(
            _Config.ROOT_DIR,
            logfile='log.tmp'
        )

        # Represents an expensive task
        e3.call('sleep 100')

        self.assertTrue(e3.is_running())

        e3.terminate()

        self.assertTrue(e3.was_terminated())

        os.remove(
            os.path.join(_Config.ROOT_DIR, 'log.tmp')
        )

    def test_close(self):
        pass

    def test_pid(self):
        if os.path.exists(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
        ):
            os.remove(
                os.path.join(_Config.ROOT_DIR, 'log.tmp')
            )

        e4 = Executor(
            _Config.ROOT_DIR,
            logfile='log.tmp'
        )

        e4.call('ls')

        self.assertTrue(
            type(e4.pid),
            int
        )

        os.remove(
            os.path.join(_Config.ROOT_DIR, 'log.tmp')
        )
