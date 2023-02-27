from selenium.webdriver.common.by import By

from controls.base_control import BaseControl
from utils.helpers.loger import log


class MenuTab(BaseControl):
    """
    Represents menu tab (mega-menu-item)
    :param name: name of the menu tab
    :param driver: instance of WebDriver
    :param parent: parent element (optional)
    """
    MENU_TAB_xpath = "//li[contains(@class, 'mega-menu-item-object') and contains(., '{}')]"
    EXPANDED_MENU_TAB_xpath = "//li[@class='mega-menu-row']"
    ARROW_DOWN_xpath = "//span[@class='mega-indicator']"
    MENU_LINK_xpath = ".//a[@class='mega-menu-link']"
    SUB_MENU_ITEM_xpath = "//li[contains(@class, 'menu-item-object-')]"

    def __init__(self, name, driver, parent=None):
        self.tab_menu_name = name
        self._menu_tab_xpath = self.MENU_TAB_xpath.format(name)
        super().__init__(driver=driver, locator=(By.XPATH, self._menu_tab_xpath), parent=parent)

        self._arrow_down = (By.XPATH, self._menu_tab_xpath + self.ARROW_DOWN_xpath)
        self._expanded_menu = (By.XPATH, self._menu_tab_xpath + self.EXPANDED_MENU_TAB_xpath)
        self._menu_tab_link = (By.XPATH, self.MENU_LINK_xpath)
        self._sub_menu_item = (By.XPATH, self.EXPANDED_MENU_TAB_xpath + self.SUB_MENU_ITEM_xpath)

    def toggle_menu_tab(self, expand=True) -> None:
        """
        Expand or collapse menu tab of the navigation control
        """
        self.wait_till_element_is_clickable()

        tab_state = self.is_expanded()
        state = "expanded" if expand else "collapsed"

        log.debug(f"Make menu tab '{self.tab_menu_name}' to '{state}' state")
        tab = self._get_web_element()
        if tab_state and not expand:
            arrow = self._get_web_element().find_elements(*self._arrow_down)
            arrow.click()
            self.wait_sub_menu_is_disappeared()
        elif not tab_state and expand:
            self._driver.hover_element(tab)
            self.is_sub_menu_displayed()
        else:
            log.debug(f"Menu tab '{self.tab_menu_name}' is already in '{state}' state")

    def is_expanded(self) -> bool:
        """
        Get menu tab state (Expanded or Collapsed)
        :return: True - if menu tab is expanded, otherwise False
        """
        log.debug(f"Get menu tab '{self.tab_menu_name}' state")
        self.wait_till_element_is_displayed()
        self.wait_till_element_is_clickable()
        state = self._get_web_element().find_element(*self._menu_tab_link).get_attribute("aria-expanded")
        return True if state == "true" else False

    def get_available_items(self) -> list[str]:
        """
        Get menu tab's available items
        :return: item list (str)
        """
        self.wait_till_element_is_displayed()
        self.wait_till_element_is_clickable()
        items = self._get_web_element().find_elements(*self._sub_menu_item)
        items = [item.text for item in items if item.text]
        return items

    def is_expandable(self) -> bool:
        """
        Check if menu tab is expandable (has 'arrow-down' element)
        :return True if sub menu has 'arrow-down' element, otherwise False
        """
        arrow_down = BaseControl(driver=self._driver, locator=self._arrow_down)
        return arrow_down.wait_till_element_exists(timeout=1)

    def is_displayed(self) -> bool:
        """
        Check if menu tab is displayed
        :return True if sub menu is visible, otherwise False
        """
        log.debug(f"Check if menu tab '{self.tab_menu_name}' is displayed on the page")
        return self.wait_till_element_is_displayed()

    def is_sub_menu_displayed(self) -> bool:
        """
        Check if sub menu is displayed
        :return True if sub menu is visible, otherwise False
        """
        self.wait_till_element_is_displayed()
        return self._driver.wait_till_element_is_displayed(self._expanded_menu)

    def wait_sub_menu_is_disappeared(self) -> bool:
        """
        Check if sub menu is disappeared
        :return False - if sub menu is displayed, otherwise True
        """
        log.debug(f"Waiting for the sub menu disappearance of '{self.tab_menu_name}' menu tab")
        return self._driver.wait_till_element_disappear(self._expanded_menu)
