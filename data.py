# data.py

BASE_URL = "https://stellarburgers.education-services.ru"

# Эндпоинты
REGISTER_ENDPOINT = "/api/auth/register"
LOGIN_ENDPOINT = "/api/auth/login"
ORDERS_ENDPOINT = "/api/orders"

# Сообщения об ошибках
MSG_USER_EXISTS = "User already exists"
MSG_REQUIRED_FIELDS = "Email, password and name are required fields"
MSG_INVALID_CREDENTIALS = "email or password are incorrect"
MSG_INGREDIENTS_REQUIRED = "Ingredient ids must be provided"

# Валидные ID ингредиентов (можно взять из документации или с сервера)
VALID_INGREDIENT_IDS = [
    "60d3b41abdacab0026a733c6",
    "609646e4dc916e00276b2870"
]
INVALID_INGREDIENT_HASH = "invalid_hash_123"