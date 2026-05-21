"""Shipping cost calculator used for the T10 AI-assisted testing project."""

VALID_DELIVERY_TYPES = {"standard", "express", "same_day"}
VALID_CUSTOMER_TYPES = {"regular", "premium"}
VALID_AREA_TYPES = {"urban", "rural"}


def calculate_shipping_cost(
    weight_kg: float,
    distance_km: float,
    delivery_type: str,
    customer_type: str,
    area_type: str,
) -> float:
    """Calculate the final shipping cost for one package.

    Rules:
    - base cost = 10 + weight_kg * 2 + distance_km * 0.5
    - express delivery adds 50%
    - same-day delivery adds 100%
    - premium customers receive a 20% discount
    - rural deliveries add a fixed 15 currency-unit fee
    """
    if weight_kg <= 0:
        raise ValueError("weight_kg must be greater than 0")

    if distance_km <= 0:
        raise ValueError("distance_km must be greater than 0")

    if delivery_type not in VALID_DELIVERY_TYPES:
        raise ValueError("delivery_type must be standard, express, or same_day")

    if customer_type not in VALID_CUSTOMER_TYPES:
        raise ValueError("customer_type must be regular or premium")

    if area_type not in VALID_AREA_TYPES:
        raise ValueError("area_type must be urban or rural")

    cost = 10 + weight_kg * 2 + distance_km * 0.5

    if delivery_type == "express":
        cost *= 1.4
    elif delivery_type == "same_day":
        cost *= 2

    if customer_type == "premium":
        cost *= 0.8

    if area_type == "rural":
        cost += 15

    return round(cost, 2)
