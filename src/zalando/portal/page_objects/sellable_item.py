from selenium.webdriver.common.by import By

from src.zalando.portal.page_objects.page_object import PageObject


class SellableItem(PageObject):

    def __init__(self, pytest, name="", price=0, smthelse=None):
        super().__init__(pytest)

    def add2cart(self):
        self.wait_for_clickable(By.ID, "z-pdp-topSection-addToCartButton").click()
        self.wait_for_element(By.XPATH, "//button[@id='z-pdp-topSection-addToCartButton'][contains(@class, 'success')]")
