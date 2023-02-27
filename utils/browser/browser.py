import selenium.webdriver.support.expected_conditions as EC

from datetime import datetime

from selenium import webdriver
from selenium.common import WebDriverException, StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.browser.web_driver_extention import ExtendedEventDriver
from utils.helpers.loger import log


class Browser:
    def __init__(self):
        self._driver = self._set_browser()

    @staticmethod
    def _set_browser() -> ExtendedEventDriver:
        """
        :return: chrome webdriver instance
        """
        ChromeDriverManager().install()
        driver = ExtendedEventDriver(webdriver.Chrome(executable_path="chromedriver"), EventListener())
        try:
            driver.maximize_window()
            log.debug(f"Get window size: {driver.get_window_size()}")
        except WebDriverException:
            log.debug("Set window size 1920x1080")
            driver.set_window_size(1920, 1080)
        return driver

    def get_browser(self):
        """
        :return: configured webdriver
        """
        return self._driver


class EventListener(AbstractEventListener):

    def __init__(self):
        self.start_time = None

    def before_find(self, by, value, driver):
        self.start_time = datetime.now()
        wait = WebDriverWait(driver, timeout=1,
                             ignored_exceptions=(StaleElementReferenceException, NoSuchElementException))
        try:
            wait.until(EC.visibility_of_element_located((by, value)))
        except TimeoutException:
            pass

    def _set_browser(self, by, value, driver):
        assert driver is not None
        self.end_time = (datetime.now() - self.start_time).total_seconds()
        if self.end_time > 5:
            log.warning("ATTENTION! Finding element/elements took more then 5 seconds. Actual time is: {}. "
                        "\nElement: {}. ".format(self.end_time, (by, value)))
