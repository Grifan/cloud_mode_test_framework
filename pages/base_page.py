from configs.config import SITE_URL
from utils.helpers.loger import log


class BasePage:
    """This class is the parent class for all the test framework pages"""
    """Consists of general functionality (available for all inherited pages)"""

    def __init__(self, driver, page_route):
        self.driver = driver
        self._url = f"{SITE_URL}/{page_route}"
        self.open()

    def get_url(self):
        return self._url

    def open(self):
        log.debug(f"Open {self._url} page")
        self.driver.get(self._url)
