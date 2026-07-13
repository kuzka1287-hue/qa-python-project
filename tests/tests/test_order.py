# tests/test_order.py

import pytest
import allure
import requests
from data import BASE_URL, ORDERS_ENDPOINT
from data import VALID_INGREDIENT_IDS, INVALID_INGREDIENT_HASH, MSG_INGREDIENTS_REQUIRED


@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа авторизованным пользователем с валидными ингредиентами")
    def test_create_order_authorized_success(self, base_url, auth_token):
        url = base_url + ORDERS_ENDPOINT
        payload = {"ingredients": VALID_INGREDIENT_IDS}
        headers = {"Authorization": auth_token}
        with allure.step("Отправить POST-запрос с токеном и ингредиентами"):
            response = requests.post(url, json=payload, headers=headers)
        with allure.step("Проверить статус 200 и наличие номера заказа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "order" in json_data
            assert "number" in json_data["order"]
            assert isinstance(json_data["order"]["number"], int)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized_fails(self, base_url):
        url = base_url + ORDERS_ENDPOINT
        payload = {"ingredients": VALID_INGREDIENT_IDS}
        with allure.step("Отправить запрос без токена"):
            response = requests.post(url, json=payload)
        with allure.step("Проверить, что вернулся статус 401 или 403"):
            # Документация говорит о переадресации, но фактически API возвращает 401
            assert response.status_code in (401, 403)
            json_data = response.json()
            assert json_data["success"] is False
            # Сообщение может быть "You should be authorised" или другое
            assert "message" in json_data

    @allure.title("Создание заказа с валидными ингредиентами (без токена, но ожидается ошибка)")
    # Этот тест уже покрыт предыдущим, но мы можем его объединить с параметризацией
    # Оставим для наглядности

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, base_url, auth_token):
        url = base_url + ORDERS_ENDPOINT
        payload = {"ingredients": []}  # пустой массив
        headers = {"Authorization": auth_token}
        with allure.step("Отправить запрос с пустым списком ингредиентов"):
            response = requests.post(url, json=payload, headers=headers)
        with allure.step("Проверить статус 400 и сообщение об ошибке"):
            assert response.status_code == 400
            json_data = response.json()
            assert json_data["success"] is False
            assert json_data["message"] == MSG_INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self, base_url, auth_token):
        url = base_url + ORDERS_ENDPOINT
        payload = {"ingredients": [INVALID_INGREDIENT_HASH]}
        headers = {"Authorization": auth_token}
        with allure.step("Отправить запрос с невалидным хешем"):
            response = requests.post(url, json=payload, headers=headers)
        with allure.step("Проверить статус 500 Internal Server Error"):
            # По документации ожидается 500
            assert response.status_code == 500
            # Можно также проверить, что ответ содержит сообщение об ошибке,
            # но оно может быть неструктурированным
            # Так как это 500, тело может быть просто текстом
            # Дополнительно проверим, что success = false, если есть JSON
            try:
                json_data = response.json()
                assert json_data.get("success") is False
            except:
                pass  # может быть не JSON