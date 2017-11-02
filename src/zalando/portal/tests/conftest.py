import logging
import uuid
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from src.zalando.portal.page_objects.login_form import LoginForm
from src.zalando.portal.page_objects.sellable_item import SellableItem
from src.zalando.portal.page_objects.search import Search
from src.zalando.portal.page_objects.page_object import PageObject
from src.zalando.portal.page_objects.wishlist import Wishlist
from src.zalando.portal.page_objects.cart import Cart

logging.basicConfig(level=logging.DEBUG)


# Private Methods
def execute(self, command, params=None):
    """Executes a command against the underlying HTML element.
    Args:
      command: The name of the command to _execute as a string.
      params: A dictionary of named parameters to send with the command.

    Returns:
      The command's JSON response loaded into a dictionary object.
    """
    sleep(1)
    if not params:
        params = {}
    params['id'] = self._id
    return self._parent.execute(command, params)

WebElement._execute = execute


def pytest_addoption(parser):
    parser.addoption("--address", action="store", default="nevsky 2",
                     help=("Customer address. Should be real and resolvable on the map. "))
    parser.addoption("--driverName", action="store", default="New Driver", help=("Driver name."))
    parser.addoption("--vehicleTitle", action="store", default="Kamaz 4308", help=("Vehicle Title"))
    parser.addoption("--vin", action="store", default="00000010000000000000001", help=("Vehicle VIN number"))
    parser.addoption("--updates", action="store", default="", help=("Updates data"))
    parser.addoption("--user", action="store", default="manager", help=("Cloud user"))
    parser.addoption("--device-id", help="Id of testing device", default="hmirig")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    test_name = item.funcargs.get("Name", "")
    test_steps = item.funcargs.get("Steps", [])

    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        # always add url to report
        extra.append(pytest_html.extras.url(pytest.driver.current_url, "Final url"))
        extra.append(pytest_html.extras.image(pytest.driver.get_screenshot_as_base64(), ''))
        # DO NOT DELETE - useful example for additional HTML inside report:
        xfail = hasattr(report, 'wasxfail')
        if xfail or report.failed:
            extra.append(pytest_html.extras.html('<div><h2 style="color: red; ">{}</h2></div>'.format(test_name)))
        elif report.passed:
            extra.append(pytest_html.extras.html('<div><h2 style="color: black; text-decoration: underline">{}</h2></div>'.format(test_name)))
        pytest_html.extras.html('<div style="color: black; margin: 10px;">'.format(test_name))
        for step in test_steps:
            extra.append(pytest_html.extras.html('<p style="margin: 5px;">{}</p>'.format(step)))
        pytest_html.extras.html('</div>')
        report.extra = extra


@pytest.fixture(scope='function')
def tearupdown(request):
    setup(request)
    def fin():
        pytest.driver.quit()

    request.addfinalizer(fin)
    return


def setup(request):
    sleep(30)
    pytest.logger = logging.getLogger('TestSession')
    pytest.logger.setLevel("DEBUG")
    pytest.client_identifier = 'pytest'
    pytest.client_secret = str(uuid.uuid4())
    pytest.user = "nikikikita@gmail.com"
    pytest.password = "abcABC123"

    chrome_options = Options()
    chrome_options.add_argument("test-type")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("disable-extensions")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-default-apps")
    # chrome_options.add_argument("disable-gpu")
    # chrome_options.add_argument("remote-debugging-port=9222")
    chrome_options.add_argument("test-type=browser")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("window-size=1680,1624")
    pytest.driver = webdriver.Chrome(chrome_options=chrome_options)
    pytest.wait = WebDriverWait(pytest.driver, 30)
    # pytest.driver.set_window_size(1280, 1024)

    # pytest.test_data_root = os.environ.get('TEST_HOME') + "/data"
    # setup default page objects
    pytest.page = PageObject(pytest)
    pytest.search = Search(pytest)
    pytest.sellable_item = SellableItem(pytest)
    pytest.cart = Cart(pytest)
    pytest.wishlist = Wishlist(pytest)
    pytest.login_form = LoginForm(pytest)
    pytest.page.goto_host()
