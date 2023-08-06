from requests import HTTPError


class AutoRiaHTTPError(HTTPError):

    def __init__(self, *args, **kwargs):
        super(AutoRiaHTTPError, self).__init__(*args, **kwargs)

        self.message = self.response.json()['error']["message"]
        self.code = self.response.json()['error']["code"]
        self.status_code = self.response.status_code

    def __str__(self):
        return f"AutoRIA Error: {self.code} - {self.message}"
