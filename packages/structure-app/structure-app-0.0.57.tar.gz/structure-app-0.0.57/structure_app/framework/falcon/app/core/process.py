from .models import Test
from .query_managers.queryset import GenericQuery


class ProcessTest:
    """
    docstring
    """

    def health(self):
        """
        """
        message = dict(status="Services status OK")
        return message

    def create(self, data):
        create = GenericQuery(Test).save(data)
        return create

    def get_test(self, data):
        get_one = GenericQuery(Test).get(data)
        return get_one

    def filter_test(self, data):
        get_many = GenericQuery(Test).filter(data)
        return get_many

    def update_test(self, data):
        update = GenericQuery(Test).update(data)
        return update

    def delete_test(self, data):
        delete = GenericQuery(Test).delete(data)
        return delete
