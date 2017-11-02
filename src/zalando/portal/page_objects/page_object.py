import os
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

def run_js_util(driver, name):
    with open('{}/{}'.format(os.environ.get('TEST_HOME', './utils/js') + "/src/utils/js", name), 'r') as util_js:
        script = util_js.read()  # read the jquery from a file
        driver.execute_script(script)  # active the jquery lib


class PageObject(object):

    def __init__(self, pytest):
        self.pytest = pytest

    def wait_for_element(self, by, value, timeout=None):
        if timeout is not None:
            self.pytest.logger.debug(f"\nValue to wait for = {value}\n"
                                     f"timeout = {str(self.pytest.wait._timeout)}\n\n")
            wait = WebDriverWait(self.pytest.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        self.pytest.logger.debug(f"\nValue to wait for = {value}\n"
                                 f"timeout = {str(self.pytest.wait._timeout)}\n\n")
        return self.pytest.wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_clickable(self, by, value, timeout=None):
        self.pytest.logger.debug(f"\n\nValue to wait for clickable = {value}\n "
                                 f"timeout = {str(self.pytest.wait._timeout)}\n\n")
        if timeout:
            return WebDriverWait(self.pytest.driver, timeout).until(EC.element_to_be_clickable((by, value)))
        return self.pytest.wait.until(EC.element_to_be_clickable((by, value)))

    def wait_for_all_elements(self, by, value, timeout=None):
        self.pytest.logger.debug(f"\nValue to wait for = {value}\n"
                                 f"timeout = {str(self.pytest.wait._timeout)}\n\n")
        if timeout:
            return WebDriverWait(self.pytest.driver, timeout).until(EC.presence_of_all_elements_located((by, value)))
        return self.pytest.wait.until(EC.presence_of_all_elements_located((by, value)))

    def wait_while_element(self, by, value, timeout=None):
        self.pytest.logger.debug(f"\nValue to wait while = {value}\n")
        if timeout:
            return WebDriverWait(self.pytest.driver, timeout).until_not(EC.presence_of_element_located((by, value)))
        return self.pytest.wait.until_not(EC.presence_of_element_located((by, value)))

    def wait_while_visible(self, by, value):
        self.pytest.logger.debug(f"\nValue to wait while = {value}\n")
        return self.pytest.wait.until_not(EC.visibility_of_element_located((by, value)))

    def goto_host(self):
        self.pytest.driver.get("http://{}/".format(self.pytest.config.getoption('host')))

    def goto_url(self, url):
        self.pytest.driver.get("http://{host}/{url}".format(host=self.pytest.config.getoption('host'), url=url))

    def goto_cart(self):
        self.wait_for_element(By.XPATH, "//a[@classname='z-navicat-header_userAccNaviItem'][@tracking='click.header.cart']").click()
        self.wait_for_element(By.XPATH, "//h4[contains(text(), 'Warenkorb')]")

    def select_by_visible_text(self, xpath, text):
        select = Select(self.wait_for_element(By.XPATH, xpath))
        select.select_by_visible_text(text)

    def goto_wishlist(self):
        self.wait_for_element(By.XPATH,
                              "//a[@classname='z-navicat-header_userAccNaviItem'][@tracking='click.header.wishlist']").click()
        self.wait_for_element(By.XPATH, "//span[contains(text(), 'MEIN WUNSCHZETTEL')]")
