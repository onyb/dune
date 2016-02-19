from abc import ABCMeta, abstractmethod


class IUnikernelBackend(object):
    """
    Interface that must be implemented by every Unikernel Backend. It contains method stubs used by the REST API
    provider and other components.

    Redefinition of functions decorated with @asbstractmethod is compulsory.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(
            self,
            project: str,
            module: [str],
            _id: int,
            config: str,
            unikernel: str
    ) -> str:
        """
        Initialize directory structure for the unikernel, and register it to the database and scheduler.
        :param _id: ID of the unikernel
        :return: Working directory of the unikernel
        """
        pass

    @abstractmethod
    def configure(self, _id):
        """
        Configure the unikernel to be built for the specific backend
        :param _id: ID of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def compile(self, _id):
        """
        Build the unikernel
        :param _id: ID of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def optimize(self, _id):
        """
        Optimize the unikernel binary/VM by stripping off debug symbols / applying data compression, etc.
        :param _id: ID of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def start(self, _id):
        """
        Launch/boot the unikernel
        :param _id: ID of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def get_status(self, _id):
        """
        Get status of the unikernel
        :param _id: ID of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def get_log(self, _id):
        """
        Get runtime log of the unikernel
        :param _id: ID of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def stop(self, _id):
        """
        Kill execution of the unikernel
        :param _id: ID of the unikernel
        :return:
        """
        pass

    @abstractmethod
    def destroy(self, _id):
        """
        Destroy the unikernel, remove all assets, and unregister from database and scheduler.
        :param _id: ID of the unikernel
        :return:
        """
        pass
