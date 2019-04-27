from flask_api import status


class ServerException(Exception):
    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=Exception()):
        super(ServerException, self).__init__(exception)
        self._message = message
        self._status_code = status_code
        pass

    @property
    def message(self):
        return self._message

    @property
    def status_code(self):
        return self._status_code



