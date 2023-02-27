from dotmap import DotMap

from .response import Response
from utils.helpers.loger import log


class Request:
    """
    Class request builder
    :param method: requests HTTP method, requests.post, requests.get etc.
    :param base_uri: base URL for request (optional)
    :param: function which takes one parameter - requests Response object (optional)
    """

    def __init__(self, method, base_uri=""):
        self._method = method
        self._base_uri = base_uri
        self._uri = None
        self._body = None
        self._headers = {}
        self._query_params = {}

    def uri(self, *routes):
        """
        Set URI for request. Sets self.base_uri if exists
        :param routes: request URI routes. Must start with http://hostname if no base_uri was set
        """
        self._uri = self._base_uri.rstrip(r'\/') + "/" + '/'.join([route.strip("/") for route in routes]).lstrip('')

    def body(self, body):
        """
        Set request body
        :param body: either Python JSON-serializable object, DotMap object, or string
        """
        if isinstance(body, DotMap):
            body = body.toDict()
        self._body = body

    def headers(self, **headers):
        """
        Add request headers. Each method call adds new headers
        """
        self._headers.update(headers)

    def query_params(self, **query_params):
        """Add request query params. Each method call adds new query params"""
        self._query_params.update(query_params)

    def auth_token(self, token):
        """Set Bearer Authorization token header"""
        self._headers["Authorization"] = "Bearer {}".format(token)

    def send(self, **extra_params):
        """
        Send request
        :param extra_params: extra kwargs request
        :return: Response object
        """
        dis_logs = extra_params.pop("_disable_logging", False)
        if not dis_logs:
            log.debug("{method}: {uri}".format(method=self._method.__name__.upper(), uri=self._uri))
            if self._query_params:
                log.debug("QUERY_PARAMS: {}".format(self._query_params))
            if self._body:
                log.debug("BODY: {}".format(self._body))

        res = self._method(self._uri, json=self._body, headers=self._headers, params=self._query_params, **extra_params)
        return Response(res)
