from src.pricing import apply_discount

def test_apply_discount_regression():
    result = apply_discount(100.0, 10)
    # The correct discounted price should be 90 and this test should fail confirming the bug
    assert result == 90.0