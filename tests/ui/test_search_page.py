from pages.welcome_page import GeneralPage
from utils.helpers.base_test import BaseWebUITest
from utils.helpers.validator import Verify
from utils.helpers.loger import log


class TestSearchForm(BaseWebUITest):
    """
    Check if logo is visible on the general pages (Solutions, Integrations, Resources, Pricing, Company)
    """
    TEST_WORD = "azure"

    def test_search_by_word(self):
        page = GeneralPage(self.driver)
        # optional step (close irritated and not related to the test 'cookie' control
        page.reject_cookies()

        log.info("Verify search result control is not displayed on the page before test")
        Verify.false(page.is_search_result_displayed(), "Search result controls is not displayed on the page")

        log.info("Open search form")
        page.open_search_form()

        log.info("Verify search forml is displayed")
        Verify.true(page.search_input.wait_till_element_is_displayed(), "Search form is not visible")

        log.info(f"Search {self.TEST_WORD}")
        page.search_by_text(text=self.TEST_WORD)

        page.driver.set_window_size()
        page.driver.save_screenshot_as_file("search_mobile_view")

        page.driver.maximize_window()
        page.driver.save_screenshot_as_file("search_desktop_view")

        log.info("Verify search result control is displayed on the page")
        Verify.true(page.is_search_result_displayed(), "Search result control is not displayed on the page")

        log.info("Verify search result control contains more than 3 articles")
        Verify.true(len(page.get_search_result_articles()) > 3, "Search result control is not displayed on the page")
