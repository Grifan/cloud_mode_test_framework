from selenium.webdriver.common.by import By

from controls.base_control import BaseControl
from controls.button import Button
from controls.input import Input
from controls.menu_tab import MenuTab
from controls.search_results import SearchResult
from pages.base_page import BasePage
from utils.helpers.loger import log


class GeneralPage(BasePage):
    """This class is the parent class for all the test framework pages
    Consists of general functionality (available for all inherited pages)"""

    def __init__(self, driver, page_url=""):
        super().__init__(driver=driver, page_route=page_url)
        self.nav_bar = BaseControl(driver=driver, locator=(By.XPATH, "//header/nav"))
        self.logo = BaseControl(driver=driver, locator=(By.CSS_SELECTOR, "a.navbar-brand img"), parent=self.nav_bar)
        self.solutions_tab = MenuTab(driver=driver, name="Solutions", parent=self.nav_bar)
        self.integrations_tab = MenuTab(driver=driver, name="Integrations", parent=self.nav_bar)
        self.pricing_tab = MenuTab(driver=driver, name="Pricing", parent=self.nav_bar)
        self.resources_tab = MenuTab(driver=driver, name="Resources", parent=self.nav_bar)
        self.company_tab = MenuTab(driver=driver, name="Company", parent=self.nav_bar)
        self.open_search_btn = Button(driver=driver, locator=(By.CSS_SELECTOR, "button.btn-search"),
                                      parent=self.nav_bar)
        self.search_input = Input(driver=driver, locator=(By.CSS_SELECTOR, "input.input-search"))
        self.search_btn = Button(driver=driver, locator=(By.CSS_SELECTOR, "button.search-button"))
        self.search_result_cont = SearchResult(driver=driver,
                                               locator=(By.XPATH, "//section[contains(@class, 'search-results')]"))
        self.cookie_btn = \
            BaseControl(driver=self.driver,
                        locator=(By.XPATH, "//div[contains(@id,'cookie')]//a[contains(@id,'decline-button')]"))

    def is_logo_displayed(self) -> bool:
        """
        Check visibility of logo control
        :return: True if logo is visible, otherwise False
        """
        log.debug("Check visibility of logo control")
        return self.logo.wait_till_element_is_displayed()

    def get_logo_src(self) -> str:
        """
        Get company logo src attribute
        :return str: src parameter company logo element
        """
        log.debug("Get logo control 'src' parameter")
        return self.logo.get_attr("src")

    def open_search_form(self) -> None:
        """Open search ford (fade in)"""
        self.open_search_btn.wait_till_element_is_displayed()
        self.open_search_btn.click()
        self.search_input.wait_till_element_is_displayed()

    def search_by_text(self, text) -> None:
        """Set received text into search field and confirm"""
        self.search_input.send_keys(text)
        self.search_btn.click()
        self.search_input.wait_till_element_is_not_visible()

    def is_search_result_displayed(self) -> bool:
        return self.search_result_cont.wait_till_element_is_displayed(3)

    def get_search_result_articles(self) -> [str]:
        """
        Get all available articles on the page
        :return: list of articles
        """
        return self.search_result_cont.get_available_articles()

    def reject_cookies(self) -> None:
        """Method checks decline cookie button visibility, click by it and wait its disappearance"""
        if self.cookie_btn.wait_till_element_is_displayed(3):
            log.debug("Click by 'Decline' cookie button")
            self.cookie_btn.click()
            self.cookie_btn.wait_till_element_is_not_visible(3)
