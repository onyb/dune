import os

from core.api import create_app
from core.exceptions import OPAMConfigurationError, InsufficientPrivilegeError, UnikernelLibraryNotFound, \
    RedisQueueNotFound
from core.utils.check_sanity import check_environment, check_mirage, is_root, check_redis_queue


def main():
    if not check_environment():
        raise OPAMConfigurationError

    if not check_mirage():
        raise UnikernelLibraryNotFound

    if not is_root():
        raise InsufficientPrivilegeError

    if not check_redis_queue():
        raise RedisQueueNotFound

    env = os.environ.get('SITE_NAME', 'Dev')
    app = create_app(env)

    port = int(
        os.environ.get(
            'PORT',
            5000
        )
    )
    app.run(
        host='0.0.0.0',
        port=port
    )


if __name__ == "__main__":
    main()
