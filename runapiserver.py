import os

from core.api import create_app
from core.exceptions import OPAMConfigurationExeception
from core.utils.check_sanity import check_environment, check_mirage


def main():
    if not check_environment() or not check_mirage():
        raise OPAMConfigurationExeception

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
