import pytest

from utils.helpers.base_test import BaseWebUITest
from pages.welcome_page import GeneralPage
from utils.helpers.loger import log
from utils.helpers.validator import Verify

LOGO_URL = "https://web.cloudmore.com/app/uploads/2022/05/logo-cloudmore.png"
PAGE_URLS = ["solutions", "home/integrations", "resources", "pricing", "company"]


class TestMenuItems(BaseWebUITest):
    """
    Check if menu items are presented on the general pages (Solutions, Integrations, Resources, Pricing, Company)
    """

    @pytest.mark.parametrize("page_url", PAGE_URLS)
    def test_menu_items(self, page_url):
        solutions_menu_items = [
            'Subscription Management',
            'Billing Automation',
            'Customer Self-Service',
            'Private Marketplace',
            'Direct CSP Partners',
            'Managed Service Providers (MSP)',
            'Distributors',
            'Enterprises',
            'Telecom']
        integrations_menu_items = ['Microsoft CSP Billing Software',  'Acronis', 'Datto']
        resources_menu_items = ['Case Studies', 'Content Hub', 'Webinars', 'Our customers', 'More Case Studies']
        company_menu_items = ['Why Cloudmore', 'Our Team', 'Careers', 'About us']

        page = GeneralPage(self.driver, page_url)

        log.info("Verify Solutions menu tab items")
        page.solutions_tab.toggle_menu_tab()
        Verify.equals(solutions_menu_items, page.solutions_tab.get_available_items(),
                      "Solutions sub menu does not have expected items")

        log.info("Verify Integrations menu tab items")
        page.integrations_tab.toggle_menu_tab()
        Verify.equals(integrations_menu_items, page.integrations_tab.get_available_items(),
                      "Integrations sub menu does not have expected items")

        log.info("Verify Resources menu tab items")
        page.resources_tab.toggle_menu_tab()
        Verify.equals(resources_menu_items, page.resources_tab.get_available_items(),
                      "Resources sub menu does not have expected items")

        log.info("Verify Pricing menu tab items")
        Verify.false(page.pricing_tab.is_expandable(), "Pricing menu tab should not be expandable")

        log.info("Verify Company menu tab items")
        page.company_tab.toggle_menu_tab()
        Verify.equals(company_menu_items, page.company_tab.get_available_items(),
                      "Company sub menu does not have expected items")
