from selenium.common.exceptions import NoSuchElementException


class wait_for_subelement_is_displayed(object):
    """ An Expectation for checking is webelement (parent) contains visible element (child)"""
    def __init__(self, parent_element, child_locator):
        self.child = child_locator
        self.parent = parent_element

    def __call__(self, driver):
        return self.parent.find_element(*self.child).is_displayed()


class wait_for_subelement_exists(object):
    """ An Expectation for checking is webelement (parent) contains element (child) (presence in DOM model)"""
    def __init__(self, parent_element, child_locator):
        self.child = child_locator
        self.parent = parent_element

    def __call__(self, driver):
        return self.parent.find_element(*self.child)


class wait_for_subelement_is_not_displayed:
    """ An Expectation for checking is webelement (parent) contains not visible element (child)"""
    def __init__(self, parent_element, child_locator):
        self.child = child_locator
        self.parent = parent_element

    def __call__(self, driver):
        try:
            return not self.parent.find_element(*self.child).is_displayed()
        except NoSuchElementException:
            return True


class wait_for_subelement_is_clickable:
    """ An Expectation for checking is webelement (parent) contains clickable child element"""
    def __init__(self, parent_element, child_locator):
        self.child = child_locator
        self.parent = parent_element

    def __call__(self, driver):
        element = self.parent.find_element(*self.child)
        return element and element.is_enabled()


class wait_for_element_attribute:
    """ An Expectation for checking is element attribute has an expected value"""

    def __init__(self, web_element, attribute_name, expected_value):
        self.element = web_element
        self.attribute_name = attribute_name
        self.expected_value = expected_value

    def __call__(self, driver):
        return self.element.get_attribute(self.attribute_name) == self.expected_value
