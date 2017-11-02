from time import sleep

from selenium.webdriver.common.by import By

from src.zalando.portal.page_objects.page_object import PageObject


class LoginForm(PageObject):
    def __init__(self, pytest):
        super().__init__(pytest)

    def login(self, user):
        self.wait_for_clickable(By.XPATH, "//input[@name='login.email']").send_keys(user.get("username"))
        self.wait_for_clickable(By.XPATH, "//input[@name='login.password']").send_keys(user.get("password"))
        self.wait_for_clickable(By.XPATH, "//button[contains(@class, 'login_button')]").click()