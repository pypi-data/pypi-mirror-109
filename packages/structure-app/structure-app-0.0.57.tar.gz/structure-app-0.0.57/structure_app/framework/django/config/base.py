import os
import falcon_jsonify
from littlenv import littlenv
import sentry_sdk
from sentry_sdk.integrations.falcon import FalconIntegration

sentry_sdk.init(
    os.environ.get("SENTRY_DSN"),
    traces_sample_rate=1.0
)

middleware = [
    falcon_jsonify.Middleware(help_messages=True),
]

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

littlenv.load(path="/".join((BASE_DIR, "")))

# DATABASE
NAME = os.environ.get("MONGO_NAME")
HOST = os.environ.get("MONGO_HOST")
PORT = os.environ.get("MONGO_PORT")
USER = os.environ.get("MONGO_USER")
PASSWORD = os.environ.get("MONGO_PASSWORD")
