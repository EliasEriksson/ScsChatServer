import asyncio
import websockets
from django import setup
from django.conf import settings
from pathlib import Path


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent.joinpath("ScsChatServiceRoot")
    print(BASE_DIR)
    settings.configure(
        BASE_DIR=BASE_DIR,
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        },
        SECRET_KEY='73v+43nugaa7is&6!=cm6e5&aad7=_%ua2w#ug2bxq+63223du'
    )
    setup()
    import ScsChatServiceRoot.Server.server as server
    loop = asyncio.get_event_loop()
    server = websockets.serve(server.Server(loop).handle_connection, "", 2021)
    loop.run_until_complete(server)
    loop.run_forever()
