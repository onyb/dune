import os

from core.backends.IUnikernelBackend import IUnikernelBackend
from core.utils.Executor import Executor
from core.api.settings import _Config as Config  # TODO: Need to switch to proper config (Dev / Prod)


class UNIXBackend(IUnikernelBackend):
    def __init__(self, _id):
        super().__init__(_id)

    def register(self, project, module, config, unikernel):
        self.work_dir = os.path.join(
            os.path.join(
                Config.ROOT_DIR,
                project,
                *module  # Unpack list to arguments
            ),
            str(self._id)
        )

        os.makedirs(
            self.work_dir,
            exist_ok=True
        )

        self.executor = Executor(self.work_dir)

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

        return

    def configure(self):
        # TODO: Need better exception handling
        self.executor.logged_call('cat unikernel.ml')

    def compile(self):
        # TODO: Need better exception handling
        self.executor.logged_call('make')

    def optimize(self):
        self.executor.logged_call('strip ./main.native')

    def start(self):
        # FIXME: This call needs to be asynchronous
        self.executor.logged_call('./main.native')
