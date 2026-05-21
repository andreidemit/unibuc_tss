import pytest

from shipping_calculator import calculate_shipping_cost


@pytest.mark.parametrize(
    ("weight_kg", "distance_km", "expected"),
    [
        (0.01, 1, 10.52),
        (1, 0.01, 12.01),
    ],
)
def test_positive_boundary_values_are_accepted(weight_kg, distance_km, expected):
    assert calculate_shipping_cost(weight_kg, distance_km, "standard", "regular", "urban") == expected


def test_express_multiplier_is_exactly_one_point_five():
    standard_cost = calculate_shipping_cost(4, 20, "standard", "regular", "urban")
    express_cost = calculate_shipping_cost(4, 20, "express", "regular", "urban")

    assert standard_cost == 28.0
    assert express_cost == 42.0
    assert express_cost == standard_cost * 1.5


def test_same_day_multiplier_is_exactly_double():
    standard_cost = calculate_shipping_cost(4, 20, "standard", "regular", "urban")
    same_day_cost = calculate_shipping_cost(4, 20, "same_day", "regular", "urban")

    assert same_day_cost == standard_cost * 2


def test_premium_discount_is_applied_after_delivery_multiplier():
    assert calculate_shipping_cost(4, 20, "express", "premium", "urban") == 33.6


def test_rural_fee_is_added_after_premium_discount():
    assert calculate_shipping_cost(4, 20, "express", "premium", "rural") == 48.6


def test_rounding_to_two_decimals_is_stable():
    assert calculate_shipping_cost(1.333, 2.777, "standard", "premium", "urban") == 11.24


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
            dict(
                weight_kg=0,
                distance_km=10,
                delivery_type="standard",
                customer_type="regular",
                area_type="urban",
            ),
            "weight_kg must be greater than 0",
        ),
        (
            dict(
                weight_kg=2,
                distance_km=0,
                delivery_type="standard",
                customer_type="regular",
                area_type="urban",
            ),
            "distance_km must be greater than 0",
        ),
        (
            dict(
                weight_kg=2,
                distance_km=10,
                delivery_type="overnight",
                customer_type="regular",
                area_type="urban",
            ),
            "delivery_type must be standard, express, or same_day",
        ),
        (
            dict(
                weight_kg=2,
                distance_km=10,
                delivery_type="standard",
                customer_type="gold",
                area_type="urban",
            ),
            "customer_type must be regular or premium",
        ),
        (
            dict(
                weight_kg=2,
                distance_km=10,
                delivery_type="standard",
                customer_type="regular",
                area_type="remote",
            ),
            "area_type must be urban or rural",
        ),
    ],
)
def test_validation_error_messages_are_exact(kwargs, message):
    with pytest.raises(ValueError) as exc_info:
        calculate_shipping_cost(**kwargs)

    assert str(exc_info.value) == message
