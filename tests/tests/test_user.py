# tests/test_user.py

import pytest
import allure
import requests
from data import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from data import MSG_USER_EXISTS, MSG_REQUIRED_FIELDS, MSG_INVALID_CREDENTIALS
from utils import generate_user_data


@allure.feature("Пользователь")
@allure.story("Регистрация")
class TestUserRegistration:

    @allure.title("Успешная регистрация уникального пользователя")
    def test_register_new_user_success(self, base_url):
        user_data = generate_user_data()
        url = base_url + REGISTER_ENDPOINT
        with allure.step("Отправить POST-запрос на регистрацию"):
            response = requests.post(url, json=user_data)
        with allure.step("Проверить статус код и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "accessToken" in json_data
            assert "refreshToken" in json_data
            assert json_data["user"]["email"] == user_data["email"]
            assert json_data["user"]["name"] == user_data["name"]

    @allure.title("Регистрация пользователя, который уже существует")
    def test_register_existing_user_fails(self, base_url, registered_user):
        # Берём данные уже зарегистрированного пользователя
        user_data = registered_user["user"]
        url = base_url + REGISTER_ENDPOINT
        with allure.step("Попытаться зарегистрироваться с теми же данными"):
            response = requests.post(url, json=user_data)
        with allure.step("Проверить статус 403 и сообщение об ошибке"):
            assert response.status_code == 403
            json_data = response.json()
            assert json_data["success"] is False
            assert json_data["message"] == MSG_USER_EXISTS

    @allure.title("Регистрация без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_register_missing_field_fails(self, base_url, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]  # Удаляем одно поле
        url = base_url + REGISTER_ENDPOINT
        with allure.step(f"Отправить запрос без поля '{missing_field}'"):
            response = requests.post(url, json=user_data)
        with allure.step("Проверить статус 403 и сообщение об ошибке"):
            assert response.status_code == 403
            json_data = response.json()
            assert json_data["success"] is False
            assert json_data["message"] == MSG_REQUIRED_FIELDS


@allure.feature("Пользователь")
@allure.story("Авторизация")
class TestUserLogin:

    @allure.title("Успешный вход существующего пользователя")
    def test_login_existing_user_success(self, base_url, registered_user):
        user_data = registered_user["user"]
        url = base_url + LOGIN_ENDPOINT
        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        with allure.step("Отправить POST-запрос на логин"):
            response = requests.post(url, json=login_payload)
        with allure.step("Проверить статус 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "accessToken" in json_data
            assert "refreshToken" in json_data
            assert json_data["user"]["email"] == user_data["email"]
            assert json_data["user"]["name"] == user_data["name"]

    @allure.title("Вход с неверным логином или паролем")
    @pytest.mark.parametrize("wrong_field, wrong_value", [
        ("email", "wrong@mail.ru"),
        ("password", "wrong_password")
    ])
    def test_login_invalid_credentials_fails(self, base_url, registered_user, wrong_field, wrong_value):
        user_data = registered_user["user"]
        url = base_url + LOGIN_ENDPOINT
        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        login_payload[wrong_field] = wrong_value  # подменяем поле на неверное
        with allure.step(f"Отправить запрос с неверным полем '{wrong_field}'"):
            response = requests.post(url, json=login_payload)
        with allure.step("Проверить статус 401 и сообщение об ошибке"):
            assert response.status_code == 401
            json_data = response.json()
            assert json_data["success"] is False
            assert json_data["message"] == MSG_INVALID_CREDENTIALS