# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        element = self.find_element(locator)
        self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def get_text(self, locator):
        return self.find_element(locator).text

    def get_attribute(self, locator, attribute):
        return self.find_element(locator).get_attribute(attribute)

    def wait_for_invisibility(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))