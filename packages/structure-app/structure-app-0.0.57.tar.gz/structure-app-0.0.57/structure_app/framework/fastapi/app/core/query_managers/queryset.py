from .mixin_queryset import Query


class GenericQuery(Query):

    def __init__(self, entity, message=None):
        self.entity = entity
        self.message = message

    def save(self, data):
        try:
            _intance = self.entity.objects.create(**data)
            return _intance
        except Exception:
            raise Exception(self.message)

    def get(self, data):
        try:
            _intance = self.entity.objects.get(**data)
            return _intance
        except self.entity.DoesNotExist:
            raise Exception(self.message)

    def filter(self, data):
        try:
            _intance = self.entity.objects.get(**data)
            return _intance
        except self.entity.DoesNotExist:
            raise Exception(self.message)

    def update(self, filter, key, data):
        try:
            _intance = self.entity.objects(
                **filter).update_one(**{'set__{}'.format(key): data})
            return _intance
        except Exception:
            raise Exception(self.message)

    def delete(self, data):
        try:
            _intance = self.entity.objects.get(**data)
            return _intance
        except Exception:
            raise Exception(self.message)
