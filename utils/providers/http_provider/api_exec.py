import json
from utils.helpers.loger import log


class ApiException(Exception):
    """
    API exception
    :param response: Response object from requests lib
    """

    def __init__(self, response):
        log_failed_response(response)
        super().__init__("API request failed")


def log_failed_response(response):
    """
    Log errors with for failed response with request data
    :param response: requests.Response object
    """

    def parse_json(json_data):
        """
        Convert JSON string/bytes into python dict
        :param json_data: str or bytes of JSON format
        :return result dict
        """
        if isinstance(json_data, bytes):
            json_data = str(json_data, "utf8")
        try:
            return json.loads(json_data)
        except json.JSONDecodeError:
            return json.loads(json_data.replace("'", "\""))

    def prettify_body(body):
        if body is None:
            return body
        try:
            body = parse_json(body)
            body = json.dumps(body, indent=2)
        except json.JSONDecodeError:
            pass
        return body

    req_body = prettify_body(response.request.body)
    res_body = prettify_body(response.content)

    log.error("[API] Occurred an error when call the API request last")
    log.error("[API] Request - Path: '{}'".format(response.request.url))
    log.error("[API] Request - Method: '{}'".format(response.request.method))
    log.error("[API] Request - Body: '{}'".format(req_body))
    log.error("[API] Response - Status Code: '{0}' - '{1}'".format(response.status_code, response.reason))
    log.error("[API] Response - Body: '{}'".format(res_body))
