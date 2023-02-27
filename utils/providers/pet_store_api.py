from configs import config
from utils.helpers.fake_data import fake
from utils.providers.http_provider import HttpClient


class PetStoreApi(HttpClient):
    """ Pet Store API client """

    def __init__(self):
        super().__init__(base_uri=config.PS_URL)

    @staticmethod
    def _get_header():
        return {
            "X-Expires-After": fake.get_formatted_date(dt_format="%a %b %d %H:%M:%S UTC %Y", delta_in_minutes=5),
            "X-Rate-Limit": "5000"
        }

    def get_serv_status(self):
        """Create entity via POST /user request"""
        req = self.get()
        req.uri("")
        return req.send()

    def post_user(self, body, endpoint_route="user", headers=""):
        """Create a new user via POST /user request"""
        req = self.post()
        req.uri("v2", endpoint_route)
        if not headers:
            # authorization workaround
            headers = self._get_header()
        req.headers(**headers)
        req.body(body)
        return req.send()

    def put_user(self, body, user_name, endpoint_route="user", headers=""):
        """Update user via PUT /user request"""
        req = self.put()
        req.uri("v2", endpoint_route, user_name)
        if not headers:
            # authorization workaround
            headers = self._get_header()
        req.headers(**headers)
        req.body(body)
        return req.send()

    def bulk_post_user(self, body, use_array=True):
        """Create new user via POST /user/createWithArray request"""
        endpoint_route = "user/" + "createWithArray" if use_array else "createWithList"
        return self.post_user(body, endpoint_route)

    def get_user_by_name(self, name, endpoint_route="user", ):
        """Create a new user via POST /user/name request"""
        req = self.get()
        req.uri("v2", endpoint_route, name)
        return req.send()

    def get_login(self, user_name, password, endpoint_route="user/login"):
        """Logs user into the system via GET /user/login request"""
        queries = {
            "user_name": user_name,
            "password": password,
        }
        req = self.get()
        req.uri("v2", endpoint_route)
        req.query_params(**queries)
        return req.send()

    def get_logout(self, endpoint_route="user/logout"):
        """Logout user from the system via GET /user/logout request"""
        req = self.get()
        req.uri("v2", endpoint_route)
        headers = self._get_header()
        req.headers(**headers)
        return req.send()

    def delete_user(self, name, endpoint_route="user"):
        """Logout user from the system via GET /user/logout request"""
        req = self.delete()
        req.uri("v2", endpoint_route, name)
        headers = self._get_header()
        req.headers(**headers)
        return req.send()
