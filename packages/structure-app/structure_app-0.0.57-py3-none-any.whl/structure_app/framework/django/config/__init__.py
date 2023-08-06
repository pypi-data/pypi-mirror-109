
import falcon
import mongoengine
import falcon_jsonify
from spectree import SpecTree
from config import base

from config.openapi import PAGES
from config.openapi import PATH
from config.openapi import TITLE
from config.openapi import VERSION


app = application = falcon.API(
    # middleware=base.middleware
)
api = SpecTree(
    'falcon',
    title=TITLE,
    version=VERSION,
    path=PATH,
    page=PAGES["swagger"]
)

# routing
from app.api.v1 import urls

mongoengine.connect(
    base.NAME,
    host=base.HOST,
    port=27017,
    username=base.USER,
    password=base.PASSWORD
)
