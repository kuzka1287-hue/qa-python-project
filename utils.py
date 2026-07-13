# utils.py

import random
import string

def generate_random_string(length=8):
    """Генерирует случайную строку из букв и цифр."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data():
    """Генерирует уникальные данные для пользователя."""
    random_part = generate_random_string(6)
    return {
        "email": f"test_{random_part}@yandex.ru",
        "password": "password123",
        "name": f"User_{random_part}"
    }