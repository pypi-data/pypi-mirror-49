class HASL_Error(Exception):
    """Base class for SL exceptions."""
    def __init__(self, code, message, details):
        self._code = code
        self._message = message
        self._details = details

    def __str__(self):
        return "HASL_Error {0}: {1}".format(self._code, self._message)

    @property
    def details(self):
        return self._details

    @property
    def message(self):
        return self._message

    @property
    def code(self):
        return self._code


class HASL_API_Error(HASL_Error):
    """An api-level exception occured."""
    def __str__(self):
        return "HASL_API_Error {0}: {1}".format(self._code, self._message)


class HASL_HTTP_Error(HASL_Error):
    """An http-level exception occured."""
    def __str__(self):
        return "HASL_HTTP_Error {0}: {1}".format(self._code, self._message)
