# tests/test_ingredient_counter.py

import allure
from pages.main_page import MainPage

@allure.feature("Конструктор")
@allure.story("Счётчик ингредиентов")
class TestIngredientCounter:

    @allure.title("Счётчик ингредиента увеличивается при добавлении")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        ingredient_name = "Говяжий метеорит"  # пример
        # Получаем текущее значение счётчика
        initial_counter = main_page.get_ingredient_counter(ingredient_name)
        initial_value = int(initial_counter) if initial_counter.isdigit() else 0

        # Добавляем ингредиент (например, кликаем по нему)
        main_page.add_ingredient_to_order(ingredient_name)

        # Получаем новое значение счётчика
        new_counter = main_page.get_ingredient_counter(ingredient_name)
        new_value = int(new_counter) if new_counter.isdigit() else 0

        assert new_value == initial_value + 1, "Счётчик не увеличился"