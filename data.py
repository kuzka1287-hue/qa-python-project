# data.py

BASE_URL = "https://stellarburgers.education-services.ru"  # замените на реальный URL

# API-эндпоинты для создания пользователя
REGISTER_ENDPOINT = "/api/auth/register"
LOGIN_ENDPOINT = "/api/auth/login"
ORDERS_ENDPOINT = "/api/orders"

# Валидные ID ингредиентов (можно взять из документации)
INGREDIENT_IDS = [
    "60d3b41abdacab0026a733c6",
    "609646e4dc916e00276b2870"
]