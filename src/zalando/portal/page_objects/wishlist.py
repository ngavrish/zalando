from time import sleep

from selenium.webdriver.common.by import By

from src.zalando.portal.page_objects.page_object import PageObject


class Wishlist(PageObject):

    def __init__(self, pytest):
        super().__init__(pytest)

    def validate_sellable_item(self, item):
        assert True

    def clear_items(self):
        items = self.wait_for_all_elements(By.XPATH, "//div[contains(@class, 'icon_remove')]")
        for item in items:
            item.click()
        self.wait_for_element(By.XPATH, "//span[text()='Dein Wunschzettel ist noch leer']")