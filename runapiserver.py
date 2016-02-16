import os

from core.api import create_app

env = os.environ.get('SITE_NAME', 'Dev')
app = create_app(env)

if __name__ == "__main__":
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
