import pytest

from configs.config import SITE_URL
from utils.helpers.base_test import BaseWebUITest
from pages.welcome_page import GeneralPage
from utils.helpers.loger import log
from utils.helpers.validator import Verify

LOGO_URL = f"{SITE_URL}/app/uploads/2022/05/logo-cloudmore.png"
PAGE_URLS = ["solutions", "home/integrations", "resources", "pricing", "company"]


class TestCompanyLogo(BaseWebUITest):
    """
    Check if logo is visible on the general pages (Solutions, Integrations, Resources, Pricing, Company)
    """
    @pytest.mark.parametrize("page_url", PAGE_URLS)
    def test_company_logo_presence(self, page_url):
        page = GeneralPage(self.driver, page_url)

        log.info("Verify company logo element presence")
        Verify.true(page.is_logo_displayed(), "Company logo element is not displayed on the page")
        Verify.equals(LOGO_URL, page.logo.get_attr("src"), "Logo element has incorrect src parameter")
