from .process import ProcessTest


class Handler:
    """
    docstring
    """
    @staticmethod
    def status():
        _status = ProcessTest().health()
        return _status
