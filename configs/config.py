from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_environment(env_variable):
    return getenv(env_variable)


SITE_URL = get_environment('CM_URL') or 'https://web.cloudmore.com'
PS_URL = get_environment('PS_URL') or 'https://petstore.swagger.io'
