#import unittest
import pytest
from src.pricing import parse_price
from src.pricing import format_currency
from src.pricing import apply_discount
from src.pricing import add_tax
from src.pricing import bulk_total


def test_parse_price_valid():
    assert parse_price("$1,234.50") == 1234.50
    assert parse_price("12.5") == 12.5
    assert parse_price("$0.99") == 0.99
    assert parse_price("$12,34,56") == 123456.0

def test_parse_invalid():
    with pytest.raises(ValueError):
        parse_price("") # testing an empty string

    with pytest.raises(ValueError):
        parse_price("abc")

def test_format_currency():
    assert format_currency(1234.50) == "$1,234.50"
    assert format_currency(12.5) == "$12.50"
    assert format_currency(0.99) == "$0.99"
    assert format_currency(123456.0) == "$123,456.00"

def test_apply_discount():
    assert apply_discount(100, 10) == 90.0
    assert apply_discount(40, 0) == 40.0
    assert apply_discount(50, 100) == 0.0

    with pytest.raises(ValueError):
        apply_discount(45, -10)

def test_add_tax():
    # Normal tax calculation
    assert add_tax(100) == pytest.approx(107.0)
    assert add_tax(53) == pytest.approx(56.71)

    # custom tax rate
    assert add_tax(100, 0.1) == pytest.approx(110.0)
    assert add_tax(200, 0.2) == pytest.approx(240.0)

    # 0% tax rate --> price unchanged
    assert add_tax(100, 0) == pytest.approx(100.0)
    assert add_tax(50, 0) == pytest.approx(50.0)

    # Negative tax rate should raise a ValueError
    with pytest.raises(ValueError):
        add_tax(100, -0.02)

def test_bulk_total():
    # simple list with a default discount of 0%, default tax with 7%
    prices = [11, 22, 33]
    expected_total =  66 * 1.07
    assert bulk_total(prices) == pytest.approx(expected_total)

    # simple list with a discount and this should fail because of the bug in the apply_discount function
    prices = [40, 50]
    expected_total = (40 + 50 - (40 + 50) * 0.11) * 1.07
    assert bulk_total(prices, discount_percent=11) == pytest.approx(expected_total)






