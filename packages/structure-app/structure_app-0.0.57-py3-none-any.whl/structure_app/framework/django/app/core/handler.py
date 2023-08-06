from .process import ProcessTest


class Handler:
    """
    docstring
    """
    @staticmethod
    def status():
        _status = ProcessTest().health()
        return _status

    @staticmethod
    def create():
        _status = ProcessTest().create()
        return _status

    @staticmethod
    def get():
        _status = ProcessTest().get_test()
        return _status

    @staticmethod
    def filter():
        _status = ProcessTest().filter_test()
        return _status

    @staticmethod
    def update():
        _status = ProcessTest().update_test()
        return _status

    @staticmethod
    def delete():
        _status = ProcessTest().delete_test()
        return _status
