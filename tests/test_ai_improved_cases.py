import pytest

from shipping_calculator import calculate_shipping_cost


def test_same_day_delivery_doubles_base_cost():
    assert calculate_shipping_cost(2, 10, "same_day", "regular", "urban") == 38.0


def test_premium_customer_receives_twenty_percent_discount():
    assert calculate_shipping_cost(2, 10, "standard", "premium", "urban") == 15.2


def test_rural_delivery_adds_fixed_fee():
    assert calculate_shipping_cost(2, 10, "standard", "regular", "rural") == 34.0


def test_premium_rural_same_day_combination():
    assert calculate_shipping_cost(2, 10, "same_day", "premium", "rural") == 45.4


@pytest.mark.parametrize(
    ("weight_kg", "distance_km"),
    [
        (0, 10),
        (2, 0),
        (2, -5),
    ],
)
def test_non_positive_numeric_inputs_are_rejected(weight_kg, distance_km):
    with pytest.raises(ValueError):
        calculate_shipping_cost(weight_kg, distance_km, "standard", "regular", "urban")


@pytest.mark.parametrize(
    ("delivery_type", "customer_type", "area_type"),
    [
        ("overnight", "regular", "urban"),
        ("standard", "gold", "urban"),
        ("standard", "regular", "remote"),
    ],
)
def test_unknown_types_are_rejected(delivery_type, customer_type, area_type):
    with pytest.raises(ValueError):
        calculate_shipping_cost(2, 10, delivery_type, customer_type, area_type)
