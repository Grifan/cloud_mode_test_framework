import pytest

from utils.providers.pet_store_api import PetStoreApi


@pytest.fixture(scope="session")
def pet_store_api():
    return PetStoreApi()
