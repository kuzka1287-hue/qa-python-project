# pages/login_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")

    def login(self, email, password):
        self.find_element(self.EMAIL_INPUT).send_keys(email)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.LOGIN_BUTTON)