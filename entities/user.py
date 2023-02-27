from utils.helpers.fake_data import fake

"""Represents user entity payload class. Used by related fixtures and test"""


def new_user_payload():
    return {
        "id": fake.number(10),
        "username": fake.property_id(),
        "firstName": fake.word(),
        "lastName": fake.word(),
        "email": fake.email(),
        "password": fake.password(),
        "phone": fake.phone(),
        "userStatus": fake.number(8),
    }
