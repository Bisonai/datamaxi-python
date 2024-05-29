class Error(Exception):
    pass


class ClientError(Error):
    def __init__(self, status_code, error_code, error_message, header, error_data=None):
        # https status code
        self.status_code = status_code
        # error code returned from server
        self.error_code = error_code
        # error message returned from server
        self.error_message = error_message
        # the whole response header returned from server
        self.header = header
        # return data if it's returned from server
        self.error_data = error_data


class ServerError(Error):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class ParameterRequiredError(Error):
    def __init__(self, params):
        self.params = params

    def __str__(self):
        return "%s is mandatory, but received empty." % (", ".join(self.params))


class AtLeastOneParameterRequiredError(Error):
    def __str__(self):
        return "At least one parameter is required."
