import os
from datetime import datetime

from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver import ActionChains
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.wait import WebDriverWait

from configs import PROJECT_PATH
from utils.browser import expected_conditions as ec


class ExtendedEventDriver(EventFiringWebDriver):

    def save_screenshot_as_file(self, test_name) -> str | None:
        current_date = "_" + (datetime.now().strftime("%Y_%m_%d_%H-%M"))
        save_path = os.path.join(PROJECT_PATH, "screenshot_on_fail")
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        file_path = os.path.join(save_path, test_name + current_date + ".png")
        return file_path if self._driver.save_screenshot(file_path) else None

    @staticmethod
    def get_screenshot_as_bytes(file_path) -> bytearray:
        with open(file_path, 'rb') as image:
            file = image.read()
            return bytearray(file)

    def set_window_size(self, width=393, height=851) -> None:
        """
        Set current window size that webdriver is using
        :param width: desired width in pixels (int, by default=393)
        :param height: desired height in pixels (int, by default=851)
        """
        self._driver.set_window_size(width, height)

    def maximize_window(self):
        """Maximizes the current window that webdriver is using"""
        self._driver.maximize_window()

    def scroll_to_element_center(self, element):
        """
        Scroll to the exact element
        :param element: web element (e.g. driver.find_element_by_xpath("//div")
        """
        # Calculate coordinates center of view, calculate top coordinates of retrieved element,
        # Based on these coordinates perform scroll to the top of element with
        # the down shift by half of element's height
        self.execute_script(
            "var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);"
            "var elementTop = arguments[0].getBoundingClientRect().top;"
            "window.scrollBy(0, elementTop-(viewPortHeight/2));", element)

    def wait_till_element_appears(self, element, timeout=5, message=''):
        wait = WebDriverWait(self._driver, timeout=timeout,
                             ignored_exceptions=(StaleElementReferenceException,
                                                 NoSuchElementException,
                                                 TimeoutException))
        try:
            return wait.until(ec.presence_of_element_located(element), message)
        except TimeoutException:
            return None

    def wait_till_element_disappear(self, element, timeout=5, message=''):
        wait = WebDriverWait(self._driver, timeout=timeout,
                             ignored_exceptions=(StaleElementReferenceException,
                                                 NoSuchElementException,
                                                 TimeoutException))
        try:
            return wait.until_not(ec.presence_of_element_located(element), message)
        except TimeoutException:
            return None
        except NoSuchElementException:
            return None

    def wait_till_element_is_displayed(self, locator, timeout=5):
        wait = WebDriverWait(self._driver, timeout=int(timeout),
                             ignored_exceptions=(StaleElementReferenceException, NoSuchElementException))
        try:
            wait.until(ec.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_till_sub_element_is_displayed(self, parent_element, child_locator, timeout=5):
        """
        Wait till element (parent) will contain visible sub element (child)
        :param parent_element: web element
        :param child_locator: child web element locator
        :param timeout: default = 5
        :return: True - sub element is displayed, otherwise - False
        """
        wait = WebDriverWait(self, timeout=timeout,
                             ignored_exceptions=(StaleElementReferenceException,
                                                 NoSuchElementException))
        try:
            wait.until(ec.wait_for_subelement_is_displayed(child_locator=child_locator, parent_element=parent_element))
            return True
        except TimeoutException:
            return False

    def wait_till_sub_element_exists(self, parent_element, child_locator, timeout=5):
        """
        Wait till element (parent) will contain sub element (presence the child in DOM model)
        :param parent_element: web element
        :param child_locator: child web element locator
        :param timeout: default = 5
        :return: True - sub element exists inside parent, otherwise - False
        """
        wait = WebDriverWait(self, timeout=timeout,
                             ignored_exceptions=(StaleElementReferenceException,
                                                 NoSuchElementException))
        try:
            wait.until(ec.wait_for_subelement_exists(child_locator=child_locator, parent_element=parent_element))
            return True
        except TimeoutException:
            return False

    def hover_element(self, web_element):
        """
        This method hover retrieved web element
        :param web_element: Web element for hovering
        """
        if isinstance(web_element, EventFiringWebElement):
            web_element = web_element.wrapped_element
        ActionChains(self._driver).move_to_element(web_element).perform()

    def wait_till_sub_element_is_not_displayed(self, parent_element, child_locator, timeout=5):
        """
        Wait till element (parent) will contain visible sub element (child)
        :param parent_element: web element
        :param child_locator: child web element locator
        :param timeout: default = 5
        :return: True - sub element is displayed, otherwise - False
        """
        wait = WebDriverWait(self._driver, timeout=timeout,
                             ignored_exceptions=(StaleElementReferenceException,))
        try:
            wait.until(ec.wait_for_subelement_is_not_displayed(child_locator=child_locator,
                                                               parent_element=parent_element))
            return True
        except TimeoutException:
            return False

    def wait_till_sub_element_is_clickable(self, parent_element, child_locator, timeout=5):
        """
        Wait till element (parent) will contain clickable sub element (child)
        :param parent_element: web element
        :param child_locator: child web element locator
        :param timeout: default = 5
        :return: True - sub element is displayed, otherwise - False
        """
        wait = WebDriverWait(self._driver, timeout=timeout,
                             ignored_exceptions=(StaleElementReferenceException,
                                                 NoSuchElementException))
        try:
            wait.until(ec.wait_for_subelement_is_clickable(child_locator=child_locator, parent_element=parent_element))
            return True
        except TimeoutException:
            return False
