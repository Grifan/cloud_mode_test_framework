from controls.base_control import BaseControl


class Input(BaseControl):
    """
    Classic HTML input.
    :param driver: instance of WebDriver
    :param locator: custom tuple locator for input
    :param parent: parent element (optional)
    """
    def __init__(self, driver, locator=None, parent=None):
        super().__init__(driver=driver, locator=locator, parent=parent)

    def send_keys(self, symbols, clear=True, use_js=False):
        """
        Input value to element using WebElement's method 'send_keys'
        :param symbols: symbols to input
        :param clear: if True - clear input before entering keys
        :param use_js: if True - set value using javascript
        """
        self.wait_till_element_is_clickable(2)
        element = self._get_web_element()
        if clear:
            element.clear()

        if not use_js:
            return element.send_keys(symbols)

        symbols = str(symbols)
        last_symbol = symbols[-1]
        symbols = symbols[:-1]
        self._driver.js_set_value_in_text_box(element, symbols)
        return element.send_keys(last_symbol)
