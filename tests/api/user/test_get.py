from utils.helpers.fake_data import fake
from utils.helpers.validator import Verify


def test_get_service_status(pet_store_api):
    """GET. Pet Store service status"""
    response = pet_store_api.get_serv_status()
    Verify.equals(200, response.status,
                  f"Health check for Pet Store was failed. Response status code {response.status}")


# todo endpoint works, but in fact there is no auth validation for other POST/PUT endpoints
def test_get_user_log_in(pet_store_api, create_user_ro):
    """GET. Log in user into the system"""
    expiration_date_format = "%a %b %d %H:%M:%S UTC %Y"
    _, payload = create_user_ro

    response = pet_store_api.get_login(user_name=payload["username"],
                                       password=payload["password"])

    Verify.equals(200, response.status, "GET user login response status code is incorrect")
    Verify.dict_contains_key("X-Expires-After", response.header,
                             "Response header does not have 'X-Expires-After' parameter")
    Verify.dict_contains_key("X-Rate-Limit", response.header,
                             "Response header does not have 'X-Rate-Limit' parameter")
    Verify.date_in_format(response.header["X-Expires-After"], expiration_date_format,
                          "Incorrect 'X-Expires-After' date format")
    Verify.equals(response.header["X-Rate-Limit"], "5000", "Incorrect 'X-Expires-After' value")


def test_get_user_log_out(pet_store_api):
    """GET. Logout user from the system"""
    response = pet_store_api.get_logout()

    Verify.equals(200, response.status, "GET user logout response status code is incorrect")
    Verify.not_contains("X-Expires-After", response.header.keys(),
                        "Logout failed. Response header contains 'X-Expires-After' parameter")
    Verify.not_contains("X-Rate-Limit", response.header,
                        "Logout failed. Response header contains 'X-Rate-Limit' parameter")


def test_get_existed_user_by_name(pet_store_api, create_user_ro):
    """GET. Read existed user by its name"""
    _, body = create_user_ro
    response = pet_store_api.get_user_by_name(name=body['username'])
    Verify.equals(200, response.status, "Get user by name response status code is incorrect")
    Verify.dict_contains_all_keys(response.json, body,
                                  "Response json does not equal to expected payload")
    Verify.equals(body, response.json, "Received user payload not equals to expected body")
