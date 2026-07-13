# pages/main_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.modal_window import ModalWindow

class MainPage(BasePage):
    # Локаторы
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[contains(@href, '/') and contains(text(), 'Конструктор')]")
    ORDERS_FEED_BUTTON = (By.XPATH, "//a[contains(@href, '/feed') and contains(text(), 'Лента заказов')]")
    INGREDIENT_ITEM = (By.XPATH, "//div[contains(@class, 'ingredient') and contains(@data-testid, 'ingredient')]")
    INGREDIENT_NAME = (By.XPATH, ".//p[contains(@class, 'name')]")
    BUN_COUNTER = (By.XPATH, "//div[contains(@data-testid, 'bun')]//p[contains(@class, 'counter')]")
    INGREDIENT_COUNTER = (By.XPATH, "//div[contains(@data-testid, 'ingredient')]//p[contains(@class, 'counter')]")
    ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class, 'OrderDetails')]//h2")

    def go_to_constructor(self):
        self.click(self.CONSTRUCTOR_BUTTON)

    def go_to_orders_feed(self):
        self.click(self.ORDERS_FEED_BUTTON)

    def click_ingredient(self, ingredient_name):
        # Находим ингредиент по имени и кликаем
        ingredient = self.find_element((By.XPATH, f"//div[contains(@class, 'ingredient')]//p[text()='{ingredient_name}']/.."))
        ingredient.click()
        return ModalWindow(self.driver)

    def get_bun_counter(self):
        return self.get_text(self.BUN_COUNTER)

    def get_ingredient_counter(self, ingredient_name):
        locator = (By.XPATH, f"//div[contains(@data-testid, 'ingredient')]//p[text()='{ingredient_name}']/../..//p[contains(@class, 'counter')]")
        return self.get_text(locator)

    def add_ingredient_to_order(self, ingredient_name):
        # Перетаскивание или клик для добавления (зависит от реализации)
        # Предположим, что добавление происходит через клик на ингредиент и затем кнопку "Добавить"
        ingredient = self.find_element((By.XPATH, f"//div[contains(@class, 'ingredient')]//p[text()='{ingredient_name}']/.."))
        ingredient.click()
        # Кнопка "Добавить" может быть внутри модалки, но по заданию просто увеличивается счётчик
        # Поэтому мы просто кликнем по ингредиенту (он может сам добавляться в конструктор)

    def get_order_number_after_creation(self):
        return self.get_text(self.ORDER_NUMBER)

    def place_order(self):
        self.click(self.ORDER_BUTTON)
        # Ждём появления номера заказа
        return self.get_order_number_after_creation()
    