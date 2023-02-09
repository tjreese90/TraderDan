class OandaError(Exception):
    """Oanda Error Exception Class"""
    def __init__(self, status_code='', resp_content=''):
        """OandaError Exception raised when server returns error.
        Args:
            status_code (str): Status code retrieved from the server.
            resp_content (dict): Response's body with more detailed info about
                                 the problem that has occurred.

        """
        if resp_content:
            message = "OANDA server returned [{}] status code".format(status_code)

            if "errorCode" in resp_content:
                message += ", and API returned [{}] error code".format(resp_content["errorCode"])

            if "errorMessage" in resp_content:
                message += ", with message: ({})".format(resp_content["errorMessage"])

        else:
            message = "OANDA server returned a internal server error"

        super().__init__(message)


class EnvironmentNotFound(Exception):
    pass


class AuthError(OandaError):
    pass


class NotFound(OandaError):
    pass


class ServerError(OandaError):
    """ServerError"""
    pass
