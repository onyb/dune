import os

from core.api.settings import _Config as Config  # TODO: Need to switch to proper config (Dev / Prod)
from core.backends.IUnikernelBackend import IUnikernelBackend
from core.utils.Executor import Executor


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
        os.makedirs(
            self.work_dir,
            exist_ok=True
        )

        with open(
                os.path.join(self.work_dir, 'config.ml'),
                'w'
        ) as file:
            file.write(
                '\n'.join(config)
            )

        with open(
                os.path.join(self.work_dir, 'unikernel.ml'),
                'w'
        ) as file:
            file.write(
                '\n'.join(unikernel)
            )

        # TODO: Save to database

        # TODO: Initialize scheduler

        return None

    def configure(self) -> int:
        # TODO: Need better exception handling
        executor = Executor(self.work_dir)
        executor.logged_call('mirage configure --unix')
        return executor.pid

    def compile(self) -> int:
        # TODO: Need better exception handling
        executor = Executor(self.work_dir)
        executor.logged_call('make')
        return executor.pid

    def optimize(self) -> int:
        executor = Executor(self.work_dir)
        executor.logged_call('strip ./main.native')
        return executor.pid

    def start(self) -> int:
        # FIXME: This call needs to be asynchronous
        executor = Executor(self.work_dir)
        executor.logged_call('./main.native')
        return executor.pid
