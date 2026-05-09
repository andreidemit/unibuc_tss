import pytest

from shipping_calculator import calculate_shipping_cost


def test_standard_delivery_for_regular_urban_customer():
    assert calculate_shipping_cost(2, 10, "standard", "regular", "urban") == 19.0


def test_negative_weight_is_rejected():
    with pytest.raises(ValueError, match="weight_kg"):
        calculate_shipping_cost(-1, 10, "standard", "regular", "urban")


def test_express_delivery_adds_fifty_percent():
    assert calculate_shipping_cost(2, 10, "express", "regular", "urban") == 28.5
