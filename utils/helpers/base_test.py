import pytest

from configs import config
from utils.helpers.loger import log


@pytest.mark.usefixtures("base_driver_setup")
class BaseWebUITest:
    """Use this class when test require Selenium WebDriver (by default Chrome)"""
    log.info("Init BaseWebUITest")
    SITE_URL = config.SITE_URL
