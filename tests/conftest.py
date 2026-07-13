# tests/conftest.py

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from data import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils import generate_user_data

@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    browser_name = request.param
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        # headless можно включить для CI
        # options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    driver.get(BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture
def registered_user():
    """Создаёт пользователя через API и возвращает его данные и токен."""
    user_data = generate_user_data()
    response = requests.post(BASE_URL + REGISTER_ENDPOINT, json=user_data)
    assert response.status_code == 200, "Не удалось создать пользователя"
    json_data = response.json()
    access_token = json_data.get("accessToken")
    return {
        "user": user_data,
        "access_token": access_token,
        "refresh_token": json_data.get("refreshToken")
    }

@pytest.fixture
def logged_in_driver(driver, registered_user):
    """Авторизует драйвер через установку токена в куки."""
    token = registered_user["access_token"].replace("Bearer ", "")
    driver.add_cookie({"name": "accessToken", "value": token})
    driver.refresh()
    return driver