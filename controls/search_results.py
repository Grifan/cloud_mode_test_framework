from selenium.webdriver.common.by import By

from controls.base_control import BaseControl


class SearchResult(BaseControl):
    """
    Custom control. Represents search result container and its inner elements
    :param driver: instance of WebDriver
    :param locator: custom tuple locator
    :param parent: parent element (optional)
    """
    def __init__(self, driver, locator=None, parent=None):
        super().__init__(driver=driver, locator=locator, parent=parent)
        self.article = BaseControl(driver=driver, locator=(By.XPATH, "//article[@class='search-result']"),
                                   parent=self)

    def get_available_articles(self):
        """
        Get all options from 'Selected' list
        :return: list of options
        """
        self.wait_till_element_is_displayed()
        element = self._get_web_element()
        self._driver.wait_till_sub_element_is_displayed(element, (By.XPATH, "//article[@class='search-result']"))
        sel_option_list = element.find_elements(*(By.XPATH, "//article[@class='search-result']"))
        return [el.text for el in sel_option_list]
