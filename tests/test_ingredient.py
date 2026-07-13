# tests/test_ingredient.py

import allure
from pages.main_page import MainPage

@allure.feature("Ингредиенты")
@allure.story("Модальное окно")
class TestIngredientModal:

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_ingredient_modal_opens(self, driver):
        main_page = MainPage(driver)
        modal = main_page.click_ingredient("Флюоресцентная булка")  # пример названия
        assert modal.is_modal_displayed(), "Модальное окно не открылось"
        # Проверяем, что заголовок содержит название ингредиента
        assert "булка" in modal.get_modal_title()

    @allure.title("Закрытие модального окна по крестику")
    def test_ingredient_modal_closes(self, driver):
        main_page = MainPage(driver)
        modal = main_page.click_ingredient("Флюоресцентная булка")
        modal.close_modal()
        # Проверяем, что модалка закрылась
        assert not modal.is_modal_displayed(), "Модальное окно не закрылось"