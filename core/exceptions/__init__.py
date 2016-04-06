class UnsupportedPlatformException(Exception):
    """
    Exception raised for platforms unsupported by Dune
    """
    pass


class OPAMConfigurationError(Exception):
    """
    Exception raised if OPAM configuration is not found
    """
    pass


class InsufficientPrivilegeError(Exception):
    """
    Exception raised if API server is launched without sudo
    """
    pass


class UnikernelLibraryNotFound(Exception):
    """
    Exception raised if the unikernel build tools are not found by the API server
    """
    pass


class MessageBrokerException(Exception):
    """
    Exception raised if the message broker is not found by the API server
    """
    pass


class RedisServerNotFound(Exception):
    """
    Exception raised if the Redis Server is not running
    """
    pass


class MongoDBServerNotFound(Exception):
    """
    Exception raised if the MongoDB server is not running
    """
    pass

class RedisQueueException(MessageBrokerException):
    """
    Exception raised if the Python Redis Queue is not found by the API server, or is not running any workers
    """
