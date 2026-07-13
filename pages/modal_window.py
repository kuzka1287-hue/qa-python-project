# pages/modal_window.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ModalWindow(BasePage):
    CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'modal__close')]")
    MODAL_TITLE = (By.XPATH, "//div[contains(@class, 'modal')]//h2")
    MODAL_CONTENT = (By.XPATH, "//div[contains(@class, 'modal')]//div[contains(@class, 'content')]")

    def close_modal(self):
        self.click(self.CLOSE_BUTTON)
        self.wait_for_invisibility(self.CLOSE_BUTTON)

    def get_modal_title(self):
        return self.get_text(self.MODAL_TITLE)

    def is_modal_displayed(self):
        return self.find_element(self.MODAL_TITLE).is_displayed()