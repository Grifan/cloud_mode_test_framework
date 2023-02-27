from typing import Any

import pytest as pytest

from entities.user import new_user_payload
from utils.helpers.loger import log


@pytest.fixture(scope="session")
def create_user_ro(pet_store_api):
    payload = new_user_payload()
    log.debug(f"Create a 'read only' new user (username = '{payload['username']}')")
    response = pet_store_api.post_user(body=payload)
    return response, payload


@pytest.fixture()
def create_user(pet_store_api):
    payload = new_user_payload()
    log.debug(f"Create a new user (username = '{payload['username']}')")
    payload = payload
    response = pet_store_api.post_user(body=payload)
    return response, payload


@pytest.fixture()
def create_custom_user(pet_store_api):
    def create_user(payload):
        username = payload.get("username", '')
        log.debug(f"Create a new custom user (username = '{username}')")
        return pet_store_api.post_user(body=payload)
    return create_user


@pytest.fixture()
def get_user_payload():
    return new_user_payload()


@pytest.fixture()
def get_user_payloads(pet_store_api):
    def create_user(item_count):
        log.debug("Create a list with user payloads")
        x: list[dict[str, str | int | Any]] = []
        for i in range(item_count):
            x.append(new_user_payload())
        return x
    return create_user
