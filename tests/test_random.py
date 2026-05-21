import random

import pytest

from oracle import (
    ORACLE_AREA_TYPES,
    ORACLE_CUSTOMER_TYPES,
    ORACLE_DELIVERY_TYPES,
    expected_shipping_cost,
    expected_validation_error,
)
from shipping_calculator import calculate_shipping_cost


RANDOM_SEED = 42
VALID_RANDOM_CASES = 500
INVALID_RANDOM_CASES = 120


def _generate_valid_random_cases():
    generator = random.Random(RANDOM_SEED)
    cases = []
    for _ in range(VALID_RANDOM_CASES):
        cases.append(
            (
                round(generator.uniform(0.01, 200), 3),
                round(generator.uniform(0.01, 2500), 3),
                generator.choice(ORACLE_DELIVERY_TYPES),
                generator.choice(ORACLE_CUSTOMER_TYPES),
                generator.choice(ORACLE_AREA_TYPES),
            )
        )
    return cases


def _generate_invalid_random_cases():
    generator = random.Random(RANDOM_SEED + 1)
    invalid_delivery_types = ("overnight", "economy", "", "STANDARD")
    invalid_customer_types = ("gold", "vip", "", "PREMIUM")
    invalid_area_types = ("remote", "suburban", "", "RURAL")
    cases = []

    for _ in range(INVALID_RANDOM_CASES):
        weight_kg = round(generator.uniform(0.01, 200), 3)
        distance_km = round(generator.uniform(0.01, 2500), 3)
        delivery_type = generator.choice(ORACLE_DELIVERY_TYPES)
        customer_type = generator.choice(ORACLE_CUSTOMER_TYPES)
        area_type = generator.choice(ORACLE_AREA_TYPES)

        invalid_dimension = generator.choice(
            ("weight", "distance", "delivery_type", "customer_type", "area_type")
        )
        if invalid_dimension == "weight":
            weight_kg = generator.choice((0, -0.01, -5, -100))
        elif invalid_dimension == "distance":
            distance_km = generator.choice((0, -0.01, -10, -1000))
        elif invalid_dimension == "delivery_type":
            delivery_type = generator.choice(invalid_delivery_types)
        elif invalid_dimension == "customer_type":
            customer_type = generator.choice(invalid_customer_types)
        else:
            area_type = generator.choice(invalid_area_types)

        cases.append((weight_kg, distance_km, delivery_type, customer_type, area_type))

    return cases


@pytest.mark.parametrize(
    ("weight_kg", "distance_km", "delivery_type", "customer_type", "area_type"),
    _generate_valid_random_cases(),
)
def test_random_valid_inputs_match_independent_oracle(
    weight_kg,
    distance_km,
    delivery_type,
    customer_type,
    area_type,
):
    expected = expected_shipping_cost(
        weight_kg,
        distance_km,
        delivery_type,
        customer_type,
        area_type,
    )

    assert (
        calculate_shipping_cost(
            weight_kg,
            distance_km,
            delivery_type,
            customer_type,
            area_type,
        )
        == expected
    )


@pytest.mark.parametrize(
    ("weight_kg", "distance_km", "delivery_type", "customer_type", "area_type"),
    _generate_invalid_random_cases(),
)
def test_random_invalid_inputs_match_independent_validation_oracle(
    weight_kg,
    distance_km,
    delivery_type,
    customer_type,
    area_type,
):
    expected_error = expected_validation_error(
        weight_kg,
        distance_km,
        delivery_type,
        customer_type,
        area_type,
    )

    assert expected_error is not None
    with pytest.raises(ValueError) as exc_info:
        calculate_shipping_cost(
            weight_kg,
            distance_km,
            delivery_type,
            customer_type,
            area_type,
        )

    assert str(exc_info.value) == expected_error


def test_independent_oracle_rejects_invalid_inputs_without_calling_sut():
    with pytest.raises(ValueError, match="weight_kg"):
        expected_shipping_cost(0, 10, "standard", "regular", "urban")
