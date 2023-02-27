import allure
import pytest as pytest

from utils.browser.browser import Browser
from utils.helpers.loger import log


def pytest_runtest_setup(item):
    """
    Setup test_name_ global pytest variable
    """
    test_name = item.name.replace("test_", "")
    test_summary = item.parent.obj.__doc__.strip() if item.parent.obj.__doc__ else item.obj.__doc__.strip()
    setattr(item, "test_name_", test_name)
    log.info(f"Start test: {test_name} - {test_summary}")


@pytest.fixture()
def base_driver_setup(request):
    log.debug("Init base driver")
    test_name = request.node.test_name_
    browser = Browser()
    driver = browser.get_browser()
    request.cls.driver = driver
    yield driver
    if request.node.rep_setup.failed or request.node.rep_call.failed:
        try:
            screen_abs_path = driver.save_screenshot_as_file(test_name)
            allure.attach(driver.get_screenshot_as_bytes(screen_abs_path),
                          test_name, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print("Could not create screenshot or save html source. Error: {}. "
                  "\n May be driver was not initialized".format(e))
    driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    """
    Track test results
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)
    if not ((report.when == 'setup' and report.failed) or report.when == 'call' or report.skipped):
        return report
    test_status = str(report.outcome).title()
    test_id = item.name.replace("test_", "")
    test_summary = item.parent.obj.__doc__.strip() if item.parent.obj.__doc__ else item.obj.__doc__.strip()
    duration = report.duration
    if report.failed:
        try:
            exec_info = str(report.longrepr.reprcrash)
        except AttributeError:
            exec_info = report.longrepr.errorstring
        log.error(f"{test_id}: {exec_info}")

    log.info(f"FINISH test '{test_id} - {test_summary}'. RESULT: {test_status} (duration={duration})")
    return report
