from controls.base_control import BaseControl


class Button(BaseControl):
    """
    Represents button control
    :param driver: instance of WebDriver
    :param locator: must be a locator tuple
    :param parent: parent element (optional)
    """

    def __init__(self, driver, locator=None, parent=None):
        super().__init__(driver=driver, locator=locator, parent=parent)
