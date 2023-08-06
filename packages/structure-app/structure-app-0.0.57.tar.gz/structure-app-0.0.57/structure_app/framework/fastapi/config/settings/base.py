import os

import pymongo
from littlenv import littlenv
from mongoengine import connect, disconnect

littlenv.load()

API_VERSION = "v0.1"


async def connect_db():
    """

    :return: connect mongodb
    """
    connect(
        os.environ.get('MONGO_NAME', 'test'),
        host=os.environ.get('MONGO_HOST', 'test'),
        port=int(os.environ.get('MONGO_PORT', 'test')),
        username=os.environ.get('MONGO_USER', 'test'),
        password=os.environ.get("MONGO_PASSWORD", "test"),
        alias=os.environ.get('MONGO_NAME', 'test')
    )


async def close_db():
    disconnect(
        alias=os.environ.get('MONGO_NAME', 'test')
    )
