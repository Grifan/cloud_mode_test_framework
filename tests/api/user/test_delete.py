from utils.helpers.loger import log
from utils.helpers.validator import Verify


def test_delete_user(pet_store_api, create_user):
    """DELETE. Existing user"""
    _response, body = create_user
    user_name = body["username"]

    Verify.equals(200, _response.status, "POST a new user response status code is incorrect")

    log.info(f"Delete user by its name ('{user_name}')")
    response = pet_store_api.delete_user(user_name)
    Verify.equals(200, response.status, "DELETE user response status code is incorrect")
    Verify.dict_contains_key("message", response.json,
                             "Delete response json does not contain expected 'message' field")
    Verify.equals(user_name, response.json["message"],
                  "'message' field not contains id of deleted user")

    log.info("Verify that user was deleted")
    response = pet_store_api.get_user_by_name(name=user_name)
    Verify.equals(404, response.status, "GET deleted user response status code is incorrect")
    Verify.dict_contains_key("message", response.json,
                             "Get response json does not contain expected 'message' field")
    Verify.equals("User not found", response.json["message"],
                  "Get response 'message' field is not correct")


def test_delete_not_existed_user(pet_store_api, get_user_payload):
    """DELETE. Not existing user"""
    body = get_user_payload
    user_name = body["username"]

    log.info("Verify that user does not exist")
    response = pet_store_api.get_user_by_name(name=user_name)
    Verify.equals(404, response.status, "GET deleted user response status code is incorrect")
    Verify.dict_contains_key("message", response.json,
                             "Get response json does not contain expected 'message' field")
    Verify.equals("User not found", response.json["message"], "Get response 'message' field is not correct")

    log.info(f"Delete user by its name ('{user_name}')")
    response = pet_store_api.delete_user(user_name)
    Verify.equals(404, response.status, "DELETE user response status code is incorrect")
    Verify.equals("", response.body, "Delete response body is not empty")
