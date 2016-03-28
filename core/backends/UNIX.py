import os

from core.api.settings import _Config as Config  # TODO: Need to switch to proper config (Dev / Prod)
from core.backends.IUnikernelBackend import IUnikernelBackend
from core.utils.Executor import Executor

from core.api.Status import Status


class UNIXBackend(IUnikernelBackend):
    def __init__(
            self,
            _id,
            project,
            module
    ):
        super().__init__(_id)

        self.work_dir = os.path.join(
            os.path.join(
                Config.ROOT_DIR,
                project,
                *module  # Unpack list to arguments
            ),
            str(self._id)
        )

    def register(
            self,
            config,
            unikernel
    ):
        Status.set(self._id, Status.WAITING)

        os.makedirs(
            self.work_dir,
            exist_ok=True
        )

        with open(
                os.path.join(self.work_dir, 'config.ml'),
                'w'
        ) as file:
            file.write(config)

        with open(
                os.path.join(self.work_dir, 'unikernel.ml'),
                'w'
        ) as file:
            file.write(unikernel)


        # TODO: Initialize scheduler

        return None

    def configure(self) -> int:
        # TODO: Need better exception handling
        executor = Executor(
            cwd=self.work_dir
        )

        executor.logged_call(
            cmd='mirage configure --unix',
            logfile='configure.log'
        )

        return executor.pid

    def compile(self) -> int:
        # TODO: Need better exception handling
        executor = Executor(
            cwd=self.work_dir
        )

        executor.logged_call(
            cmd='make',
            logfile='compile.log'
        )

        return executor.pid

    def optimize(self) -> int:
        executor = Executor(
            cwd=self.work_dir
        )

        executor.logged_call(
            cmd='strip ./main.native',
            logfile='strip.log'
        )

        return executor.pid

    def start(self) -> int:
        executor = Executor(
            cwd=self.work_dir
        )

        executor.logged_call(
            cmd='./main.native',
            logfile='stdout.log',
            stderr=True  # FIXME: Mirage console prints to stderr by default
        )

        return executor.pid
