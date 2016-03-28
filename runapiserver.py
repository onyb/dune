import os

from core.api import API
from core.exceptions import OPAMConfigurationError, InsufficientPrivilegeError, UnikernelLibraryNotFound, \
    RedisServerNotFound, RedisQueueException
from core.utils.check_sanity import check_environment, check_mirage, is_root, check_redis_server, check_redis_queue


def main():
    if not check_environment():
        raise OPAMConfigurationError

    if not check_mirage():
        raise UnikernelLibraryNotFound

    if not is_root():
        raise InsufficientPrivilegeError

    if not check_redis_server():
        raise RedisServerNotFound

    if not check_redis_queue():
        raise RedisQueueException

    port = int(
        os.environ.get(
            'PORT',
            5000
        )
    )

    API().create_app()
    API().create_mongo()

    API.app.run(
        host='0.0.0.0',
        port=port
    )


if __name__ == "__main__":
    main()
