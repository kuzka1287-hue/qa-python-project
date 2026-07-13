# utils.py

import random
import string

def generate_random_string(length=8):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data():
    random_part = generate_random_string(6)
    return {
        "email": f"test_{random_part}@yandex.ru",
        "password": "password123",
        "name": f"User_{random_part}"
    }