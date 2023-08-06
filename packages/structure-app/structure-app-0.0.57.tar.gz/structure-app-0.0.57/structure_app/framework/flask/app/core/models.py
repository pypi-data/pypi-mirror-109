from mongoengine import (
    StringField,
    UUIDField,
    DateTimeField,
    BooleanField,
)

from uuid import uuid4
from datetime import datetime


class Base:
    """
    """  
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField()
    deleted_at = DateTimeField()
    active = BooleanField(default=True)
    deleted = BooleanField(default=False)
    trash = BooleanField(default=False)


class Test(Base):
    """
    """
    name = StringField()
