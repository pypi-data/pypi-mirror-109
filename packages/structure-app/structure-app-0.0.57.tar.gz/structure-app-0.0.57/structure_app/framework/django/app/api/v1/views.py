import json
import falcon
from spectree import Response
from config import api

from app.core.handler import Handler
from app.api.v1.serializers import SuccessSerializer


class HealthCheckView:
    """
    Health check resource
    """
    @api.validate(
        json=SuccessSerializer,
        resp=Response(
            HTTP_200=None,
            HTTP_403=None
        ), tags=['Status']
    )
    def on_get(self, request, response):
        _response = Handler.status()
        # _response = "OK"
        response.body = json.dumps(_response)
        response.status = falcon.HTTP_200
