from abc import ABCMeta, abstractmethod


class IUnikernelBackend(object):
    """
    Interface that must be implemented by every Unikernel Backend. It contains method stubs used by the REST API
    provider and other components.

    Redefinition of functions decorated with @asbstractmethod is compulsory.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(
            self,
            _id
    ):
        self.work_dir = None
        self.executor = None
        self._id = _id

    @abstractmethod
    def register(
            self,
            config: str,
            unikernel: str
    ) -> str:
        """
        Initialize directory structure for the unikernel, and register it to the database and scheduler.
        :return: Working directory of the unikernel
        """
        pass

    @abstractmethod
    def configure(self):
        """
        Configure the unikernel to be built for the specific backend
        :return:
        """
        pass

    @abstractmethod
    def compile(self):
        """
        Build the unikernel
        :return:
        """
        pass

    @abstractmethod
    def optimize(self):
        """
        Optimize the unikernel binary/VM by stripping off debug symbols / applying data compression, etc.
        :return:
        """
        pass

    @abstractmethod
    def start(self):
        """
        Launch/boot the unikernel
        :return:
        """
        pass

    @abstractmethod
    def get_status(self):
        """
        Get status of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def get_log(self):
        """
        Get runtime log of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Kill execution of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        Destroy the unikernel, remove all assets, and unregister from database and scheduler.
        :return:
        """
        pass
