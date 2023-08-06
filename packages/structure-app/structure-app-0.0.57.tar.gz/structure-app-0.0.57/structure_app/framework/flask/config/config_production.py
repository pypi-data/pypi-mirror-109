import os
from urllib.parse import quote_plus


# Flask
DEBUG = False
TESTING = False
DEVELOPMENT = False

# DB
MONGO_USER = quote_plus(os.environ.get('MONGO_APPLICATION_USER'))
MONGO_PASS = quote_plus(os.environ.get('MONGO_APPLICATION_PASS'))
MONGO_URI = "mongodb+srv://{}:{}@{}/{}".format(
        MONGO_USER,
        MONGO_PASS,
        os.environ.get('MONGO_HOST', 'localhost'),
        os.environ.get('MONGO_APPLICATION_DATABASE', 'local')
    )
MONGODB_CONNECT = True
MONGODB_SETTINGS = {
    'host': MONGO_URI
}

# Security
DEFAULT_USER_ADMIN_USERNAME = os.environ.get('DEFAULT_USER_ADMIN_USERNAME')
DEFAULT_USER_ADMIN_PASSWORD = os.environ.get('DEFAULT_USER_ADMIN_PASSWORD')
