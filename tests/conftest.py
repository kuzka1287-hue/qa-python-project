# tests/conftest.py

import pytest
import requests
from data import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils import generate_user_data

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def new_user_data():
    """Создаёт данные нового уникального пользователя."""
    return generate_user_data()

@pytest.fixture
def registered_user(new_user_data):
    """
    Регистрирует пользователя и возвращает его данные и токены.
    После теста пользователь не удаляется (для упрощения, но можно добавить удаление через API, если есть).
    """
    url = BASE_URL + REGISTER_ENDPOINT
    response = requests.post(url, json=new_user_data)
    assert response.status_code == 200, "Не удалось создать пользователя для фикстуры"
    data = response.json()
    return {
        "user": new_user_data,
        "access_token": data.get("accessToken"),
        "refresh_token": data.get("refreshToken"),
        "user_data": data.get("user")
    }

@pytest.fixture
def auth_token(registered_user):
    """Возвращает accessToken зарегистрированного пользователя."""
    return registered_user["access_token"]