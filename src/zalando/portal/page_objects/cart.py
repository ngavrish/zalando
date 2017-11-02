from time import sleep

from selenium.webdriver.common.by import By

from src.zalando.portal.page_objects.page_object import PageObject


class Cart(PageObject):

    def __init__(self, pytest):
        super().__init__(pytest)

    def change_quantity(self, amount):
        current_price = self.get_price()
        self.select_by_visible_text("//select[@class='z-coast-fjord_quantitySelect']", str(amount))
        assert current_price*amount == self.get_price()

    def get_price(self):
        return float(self.wait_for_element(By.XPATH, "//div[contains(@class, 'priceWrapper')]/span").text.split(" ")[0].
                   replace(",", "."))

    def add2wishlist(self, user=None):
        try:
            items_in_wishlist = int(self.wait_for_element(By.XPATH, "//a[@classname='z-navicat-header_userAccNaviItem']"
                                                                "[@tracking='click.header.wishlist']/span[contains(@class, "
                                                                "'userAccNaviItemCounter')]").text)
        except ValueError:
            items_in_wishlist = 0
        self.wait_for_clickable(By.XPATH, "//span[contains(@class, 'wishlistText')]").click()
        if user is not None:
            self.pytest.login_form.login(user)
            sleep(30)
        assert items_in_wishlist + 1 == int(self.wait_for_element(By.XPATH, "//a[@classname='z-navicat-header_userAccNaviItem']"
                                                            "[@tracking='click.header.wishlist']/span[contains(@class, "
                                                            "'userAccNaviItemCounter')]").text)

    def validate_cart_empty(self):
        self.wait_for_element(By.XPATH, "//div[contains(text(), 'Leg los und fülle ihn mit den neuesten Fashion Trends.')]")

