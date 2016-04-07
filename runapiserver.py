from core.api import API
from core.exceptions import *
from core.utils.check_sanity import *


def main():
    checks = [
        (
            check_environment, OPAMConfigurationError
        ),
        (
            check_mirage, UnikernelLibraryNotFound
        ),
        (
            is_root, InsufficientPrivilegeError
        ),
        (
            check_redis_server, RedisServerNotFound
        ),
        (
            check_mongod_server, MongoDBServerNotFound
        ),
        (
            check_redis_queue, RedisQueueException
        )
    ]

    for check in checks:
        if not check[0]():
            raise check[1]

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
