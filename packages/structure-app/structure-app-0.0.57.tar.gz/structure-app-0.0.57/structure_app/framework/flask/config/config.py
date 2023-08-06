"""Default config.py file"""

import os


basedir = os.path.abspath(os.path.dirname(__file__)) + '/..'


# Flask
ENV = os.environ.get('FLASK_ENV')
if not os.path.isfile(f'{basedir}/instance/config_{ENV}.py'):
    raise ValueError(f'The configuration for the FLASK_ENV={ENV} '
                     'is not defined')

DEBUG = os.environ.get('FLASK_DEBUG', False)

# Flask-CORS
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

# Cache
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
CACHE_DEFAULT_TIMEOUT = 30
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_TASK_TIME_LIMIT = 30

# DB
MONGODB_SETTINGS = {
    'host': os.environ.get('MONGO_URI')
}

# Security
DEFAULT_USER_ADMIN_USERNAME = os.environ.get('DEFAULT_USER_ADMIN_USERNAME')
DEFAULT_USER_ADMIN_PASSWORD = os.environ.get('DEFAULT_USER_ADMIN_PASSWORD')
