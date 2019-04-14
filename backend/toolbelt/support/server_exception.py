class ServerException(Exception):
    def __init__(self, message, status_code, exception=Exception()):
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



