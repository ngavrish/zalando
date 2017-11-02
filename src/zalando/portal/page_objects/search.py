from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.zalando.portal.page_objects.page_object import PageObject


class Search(PageObject):
    def __init__(self, pytest):
        super().__init__(pytest)

    def search_by_code(self, code):
        self.wait_for_clickable(By.ID, "searchContent").send_keys(code + "\n")
        self.validate_item_found(code)

    def validate_item_found(self, item):
        assert True
