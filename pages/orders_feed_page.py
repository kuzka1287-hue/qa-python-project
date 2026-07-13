# pages/orders_feed_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class OrdersFeedPage(BasePage):
    TOTAL_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за всё время')]/following-sibling::p")
    TODAY_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    ORDER_IN_WORK = (By.XPATH, "//ul[contains(@class, 'orderList')]//li[contains(@class, 'order')]")

    def get_total_orders_count(self):
        return int(self.get_text(self.TOTAL_COUNTER))

    def get_today_orders_count(self):
        return int(self.get_text(self.TODAY_COUNTER))

    def get_orders_in_work(self):
        elements = self.find_elements(self.ORDER_IN_WORK)
        return [el.text for el in elements]

    def wait_for_order_appear(self, timeout=10):
        # Ожидаем появления нового заказа в разделе "В работе"
        self.wait.until(lambda d: len(d.find_elements(*self.ORDER_IN_WORK)) > 0)