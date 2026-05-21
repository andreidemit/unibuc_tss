"""Independent oracle used by the random tests.

The production function in ``shipping_calculator`` is intentionally not used
here. The oracle repeats the public specification in a separate implementation
so random tests can compare the system under test against an independent
expected result.
"""

ORACLE_DELIVERY_TYPES = ("standard", "express", "same_day")
ORACLE_CUSTOMER_TYPES = ("regular", "premium")
ORACLE_AREA_TYPES = ("urban", "rural")


def expected_shipping_cost(
    weight_kg: float,
    distance_km: float,
    delivery_type: str,
    customer_type: str,
    area_type: str,
) -> float:
    """Return the expected shipping cost according to the public rules."""
    error = expected_validation_error(
        weight_kg=weight_kg,
        distance_km=distance_km,
        delivery_type=delivery_type,
        customer_type=customer_type,
        area_type=area_type,
    )
    if error is not None:
        raise ValueError(error)

    base_cost = 10 + (2 * weight_kg) + (0.5 * distance_km)
    delivery_multiplier_by_type = {
        "standard": 1.0,
        "express": 1.5,
        "same_day": 2.0,
    }
    customer_multiplier_by_type = {
        "regular": 1.0,
        "premium": 0.8,
    }
    area_fee_by_type = {
        "urban": 0.0,
        "rural": 15.0,
    }

    expected = base_cost
    expected *= delivery_multiplier_by_type[delivery_type]
    expected *= customer_multiplier_by_type[customer_type]
    expected += area_fee_by_type[area_type]

    return round(expected, 2)


def expected_validation_error(
    weight_kg: float,
    distance_km: float,
    delivery_type: str,
    customer_type: str,
    area_type: str,
) -> str | None:
    """Return the expected validation error message, or None for valid input."""
    if weight_kg <= 0:
        return "weight_kg must be greater than 0"
    if distance_km <= 0:
        return "distance_km must be greater than 0"
    if delivery_type not in ORACLE_DELIVERY_TYPES:
        return "delivery_type must be standard, express, or same_day"
    if customer_type not in ORACLE_CUSTOMER_TYPES:
        return "customer_type must be regular or premium"
    if area_type not in ORACLE_AREA_TYPES:
        return "area_type must be urban or rural"
    return None
