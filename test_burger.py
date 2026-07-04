# tests/test_burger.py

import pytest
from unittest.mock import Mock, patch
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


@pytest.fixture
def burger():
    """Фикстура для создания чистого бургера перед каждым тестом."""
    return Burger()


# ---- Тесты для set_buns ----

def test_set_buns(burger):
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = "white bun"
    mock_bun.get_price.return_value = 100.0

    burger.set_buns(mock_bun)

    assert burger.bun == mock_bun
    assert burger.bun.get_name() == "white bun"
    assert burger.bun.get_price() == 100.0


# ---- Тесты для add_ingredient ----

def test_add_ingredient(burger):
    mock_ingredient = Mock(spec=Ingredient)
    mock_ingredient.get_name.return_value = "cutlet"
    mock_ingredient.get_price.return_value = 150.0

    burger.add_ingredient(mock_ingredient)

    assert len(burger.ingredients) == 1
    assert burger.ingredients[0] == mock_ingredient
    assert burger.ingredients[0].get_name() == "cutlet"


# ---- Тесты для remove_ingredient ----

def test_remove_ingredient(burger):
    # Добавляем два ингредиента
    ing1 = Mock(spec=Ingredient)
    ing2 = Mock(spec=Ingredient)
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)

    burger.remove_ingredient(0)

    assert len(burger.ingredients) == 1
    assert burger.ingredients[0] == ing2


def test_remove_ingredient_out_of_range(burger):
    # Если индекс не существует, должен быть IndexError
    with pytest.raises(IndexError):
        burger.remove_ingredient(0)   # список пуст


# ---- Тесты для move_ingredient ----

def test_move_ingredient(burger):
    # Добавляем три ингредиента
    ing1 = Mock(spec=Ingredient)
    ing2 = Mock(spec=Ingredient)
    ing3 = Mock(spec=Ingredient)
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    burger.add_ingredient(ing3)

    # Перемещаем ингредиент с индекса 0 на индекс 2
    burger.move_ingredient(0, 2)

    # Ожидаемый порядок: ing2, ing3, ing1
    assert burger.ingredients[0] == ing2
    assert burger.ingredients[1] == ing3
    assert burger.ingredients[2] == ing1


def test_move_ingredient_out_of_range(burger):
    # При перемещении с несуществующим индексом также будет ошибка
    with pytest.raises(IndexError):
        burger.move_ingredient(5, 0)


# ---- Тесты для get_price (с параметризацией) ----

@pytest.mark.parametrize(
    "bun_price, ingredient_prices, expected_price",
    [
        (100.0, [50.0, 30.0], 280.0),   # 2*100 + 50 + 30 = 280
        (200.0, [], 400.0),             # только булочка (2*200)
        (150.0, [10.0, 20.0, 30.0], 360.0), # 2*150 + 10+20+30 = 360
    ]
)
def test_get_price(burger, bun_price, ingredient_prices, expected_price):
    # Мокаем булочку
    mock_bun = Mock(spec=Bun)
    mock_bun.get_price.return_value = bun_price
    burger.set_buns(mock_bun)

    # Добавляем моки ингредиентов с заданными ценами
    for price in ingredient_prices:
        mock_ing = Mock(spec=Ingredient)
        mock_ing.get_price.return_value = price
        burger.add_ingredient(mock_ing)

    actual_price = burger.get_price()
    assert actual_price == expected_price


# ---- Тесты для get_receipt (с параметризацией) ----

@pytest.mark.parametrize(
    "bun_name, ingredients_info, expected_lines",
    [
        # Случай без ингредиентов
        (
            "black bun",
            [],
            [
                "(==== black bun ====)",
                "(==== black bun ====)",
                "Price: 200.0"   # цена булочки 100 * 2 = 200
            ]
        ),
        # С одним ингредиентом (соус)
        (
            "white bun",
            [("SAUCE", "hot sauce", 100.0)],
            [
                "(==== white bun ====)",
                "= sauce hot sauce =",
                "(==== white bun ====)",
                "Price: 500.0"   # 2*200 + 100 = 500
            ]
        ),
        # С двумя ингредиентами (соус и начинка)
        (
            "red bun",
            [
                ("SAUCE", "chili sauce", 50.0),
                ("FILLING", "cutlet", 150.0)
            ],
            [
                "(==== red bun ====)",
                "= sauce chili sauce =",
                "= filling cutlet =",
                "(==== red bun ====)",
                "Price: 800.0"   # 2*300 + 50 + 150 = 800
            ]
        ),
    ]
)
def test_get_receipt(burger, bun_name, ingredients_info, expected_lines):
    # Мокаем булочку
    mock_bun = Mock(spec=Bun)
    mock_bun.get_name.return_value = bun_name
    mock_bun.get_price.return_value = 100.0 if bun_name == "black bun" else 200.0 if bun_name == "white bun" else 300.0
    burger.set_buns(mock_bun)

    # Добавляем ингредиенты
    for ing_type, ing_name, ing_price in ingredients_info:
        mock_ing = Mock(spec=Ingredient)
        mock_ing.get_type.return_value = ing_type
        mock_ing.get_name.return_value = ing_name
        mock_ing.get_price.return_value = ing_price
        burger.add_ingredient(mock_ing)

    receipt = burger.get_receipt()
    receipt_lines = receipt.split('\n')

    # Проверяем, что все ожидаемые строки присутствуют в чеке (и в правильном порядке)
    assert len(receipt_lines) == len(expected_lines), "Количество строк не совпадает"
    for expected, actual in zip(expected_lines, receipt_lines):
        assert expected == actual, f"Ожидалось: '{expected}', получено: '{actual}'"   
