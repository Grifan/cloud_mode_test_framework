
class BaseControl:
    """
    Base class for UI controls.
    Responsible for searching of an element (using parent element if needed), implements basic waiting functions.
    Each subclass have to set `_locator` field, it has to be a classic Selenium locator: tuple(By.METHOD, VALUE).
    :param driver: instance of Selenium WebDriver
    :param locator: locator tuple
    :param parent: optional argument. If given, element is searched as a child of 'parent' element.
        Can be either a locator tuple or a subclass of BaseControl.
    """

    def __init__(self, driver, locator, parent=None):
        self._driver = driver
        self.__parent = None
        self.__locator = None
        self._parent = parent
        self._locator = locator

        self._fields_timeout_seconds = 0.55

    @property
    def _locator(self):
        """Returns Control locator"""
        return self.__locator

    @_locator.setter
    def _locator(self, locator):
        """
        Set Control locator
        :param locator: tuple (By.<CSS/XPATH/etc>, 'locator')
        """
        if not isinstance(locator, tuple):
            raise ValueError("Locator must be a tuple (By.<CSS/XPATH/etc>, 'locator')")
        self.__locator = locator

    @property
    def _parent(self):
        """Return Control's parent"""
        return self.__parent

    @_parent.setter
    def _parent(self, parent):
        """
        Set Control's parent
        :param parent: either None, locator tuple or instance of BaseControl
        """
        rules = (
            parent is None,
            isinstance(parent, BaseControl),
            isinstance(parent, tuple)
        )
        if not any(rules):
            raise ValueError("Wrong parent value was given: {}. Must be either None,"
                             "subclass of BaseControl or a locator tuple".format(parent))
        self.__parent = parent

    def _get_web_element(self, timeout=15):
        """
        Waits for a parent and gets WebElement of locator
        :param timeout: timeout for wait of parent element
        :return: WebElement of _locator
        """
        return self._get_parent_element(timeout).find_element(*self._locator)

    def _get_parent_element(self, timeout=15):
        """
        Waits and retrieves WebElement of 'parent'
        :param timeout: timeout value to wait
        :return: WebElement of self._parent, or self._driver if parent is not specified
        """
        if not self._parent:
            return self._driver

        if isinstance(self._parent, BaseControl):
            parent_of_parent = self._parent._get_parent_element(timeout)
            self._driver.wait_till_sub_element_exists(parent_of_parent, self._parent._locator,
                                                      timeout)
            return parent_of_parent.find_element(*self._parent._locator)

        if isinstance(self._parent, tuple or list) and len(self._parent) == 2:
            self._driver.wait_till_element_appears(self._parent, timeout=timeout)
            return self._driver.find_element(*self._parent)

        raise ValueError("Wrong parent format given: {}. "
                         "Subclass of BaseControl or locator is required".format(self._parent))

    def wait_till_element_is_displayed(self, timeout=3):
        """
        Waits till element is displayed
        :param timeout: timeout limit for waiting of parent element and/or locator
            For example, if timeout=15, total timeout wait can be 30 seconds. 15 - for parent await,
            and 15 - for target element
        :return: True if element is displayed, False - timeout is met
        """
        return self._driver.wait_till_sub_element_is_displayed(self._get_parent_element(timeout), self._locator, timeout)

    def wait_till_element_exists(self, timeout=5):
        """
        Waits till element is exists (presence the in DOM model)
        :param timeout: timeout limit for waiting of parent element and/or locator
        :return: True if element exists, False - timeout is met
        """
        return self._driver.wait_till_sub_element_exists(self._get_parent_element(timeout), self._locator, timeout)

    def wait_till_element_is_clickable(self, timeout=5):
        """
        Waits till element is enabled/clickable
        :param timeout: timeout limit for waiting of parent element and/or locator
        :return: True if element is enabled/clickable, False - timeout is met
        """
        return self._driver.wait_till_sub_element_is_clickable(self._get_parent_element(timeout), self._locator, timeout)

    def wait_till_element_is_not_visible(self, timeout=5):
        """
        Waits till element is not visible/displayed
        :param timeout: timeout limit for waiting of parent element and/or locator
        :return: True if element is not visible/displayed, False - timeout is met
        """
        return self._driver.wait_till_sub_element_is_not_displayed(self._get_parent_element(timeout), self._locator,
                                                                   timeout)

    def get_attr(self, attr_name):
        """
        Get attribute value of WebElement
        :param attr_name: name of attribute
        :return: value of attribute
        """
        return self._get_web_element().get_attribute(attr_name)

    def click(self):
        """
        Waits for element becomes clickable and performs click
        """
        self.wait_till_element_is_clickable()
        element = self._get_web_element()
        self._driver.scroll_to_element_center(element)
        return element.click()
