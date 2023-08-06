from flask import Blueprint
from flask_restplus import Api

routes_public = Blueprint('routes_public', __name__)
api = Api(routes_public)


@routes_public.route('health')
def health_check():
    return dict(messge="Ok")
