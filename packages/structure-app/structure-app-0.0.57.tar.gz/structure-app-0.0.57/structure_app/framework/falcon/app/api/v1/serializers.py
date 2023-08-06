from pydantic import BaseModel


class SuccessSerializer(BaseModel):
    """
    serializer respuesta swagger
    """
    message: str = "OK"
