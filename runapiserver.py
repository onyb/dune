from core.api import API
from core.exceptions import *
from core.utils.Colorize import Colorize
from core.utils.check_sanity import *


def main():
    # Order of checks is important
    checks = [
        (
            check_environment,
            'Check current shell environment',
            OPAMConfigurationError
        ),
        (
            check_mirage,
            'Check MirageOS',
            UnikernelLibraryNotFound
        ),
        (
            is_not_root,
            'Check if current user is NOT "root"',
            ExcessivePrivilegeError
        ),
        (
            check_privilege,
            'Check if user "%s" has the required privilege to run APT' % getuser(),  # User cannot be "root" here
            InsufficientPrivilegeError
        ),
        (
            check_redis_server,
            'Check running instance of Redis server',
            RedisServerNotFound
        ),
        (
            check_mongod_server,
            'Check running instance of MongoDB server',
            MongoDBServerNotFound
        ),
        (
            check_redis_queue,
            'Check Python Redis Queue worker',
            RedisQueueException
        )
    ]

    print(
        ' ' + '-' * 79 + '\n',
        Colorize.light_purple('Performing startup sanity check') + '\n',
        '-' * 79
    )

    for check in checks:
        if not check[0]():
            print(
                Colorize.light_purple(' *'), check[1], '.' * (80 - len(check[1]) - 12), Colorize.red('FAILURE')
            )
            raise check[2]
        else:
            print(
                Colorize.light_purple(' *'), check[1], '.' * (80 - len(check[1]) - 12), Colorize.green('SUCCESS')
            )

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
        port=port,
        use_reloader=False
    )


if __name__ == "__main__":
    main()
