from pymongo import MongoClient
from pymongoext import Model

from config.settings.base import connect_db_mongo


class BaseMongoModel(Model):

    @classmethod
    def db(cls):
        return connect_db_mongo()
