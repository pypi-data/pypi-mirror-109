from .models import Test


class ProcessTest:
    """
    docstring
    """

    def health(self):
        """
        """
        message = dict(status="Services status OK")
        return message
