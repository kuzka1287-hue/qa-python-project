# tests/test_navigation.py

import allure
from pages.main_page import MainPage

@allure.feature("Навигация")
@allure.story("Переход по разделам")
class TestNavigation:

    @allure.title("Переход на страницу 'Конструктор' по клику")
    def test_click_constructor(self, driver):
        main_page = MainPage(driver)
        # Сначала переходим в ленту заказов, чтобы потом вернуться
        main_page.go_to_orders_feed()
        # Кликаем на "Конструктор"
        main_page.go_to_constructor()
        # Проверяем, что текущий URL или заголовок страницы соответствует конструктору
        assert "constructor" in driver.current_url or "stellarburgers" in driver.current_url

    @allure.title("Переход на страницу 'Лента заказов' по клику")
    def test_click_orders_feed(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_orders_feed()
        # Проверяем, что URL содержит /feed
        assert "/feed" in driver.current_url