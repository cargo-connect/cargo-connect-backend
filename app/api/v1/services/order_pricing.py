# app/api/v1/services/order_pricing.py
# from app.api.v1.schemas.order_pricing.PricingBase import weight


def calculate_estimated_price(delivery_type: str, distance: float,
                              weight: float = 0) -> float:
    base_prices = {
        "motorcycle": 1500.0,  # base price for motorcycle delivery
        "car": 1500.0,  # base price for car delivery
        "van": 10000.0,  # base price for van delivery
        # "pickup": 1000.0,
    }

    # Additional cost factors

    cost_per_km = {
        "motorcycle": 500.5,
        "car": 800.7,
        "van": 850.0,
        # "pickup": 10000,
    }

    # A fee based on weight
    weight_fee = 0.0
    if weight > 0:
        weight_fee = weight * 500.0  # for example, 500 naira per kg

    # Retrieve the base price and per km cost
    base_price = base_prices.get(delivery_type, 1500.0)  # Fallback default
    per_km_cost = cost_per_km.get(delivery_type, 500.5)

    # A simple formula: base price + (distance * per km cost) + weight fee
    estimated_price = base_price + (distance * per_km_cost) + weight_fee
    return round(estimated_price, 2)


# def calculate_estimated_price(weight_kg: float, distance_km: float, speed: str = "standard", package_type: str = "regular") -> float:
#     base_fee = 1000
#     weight_fee = weight_kg * 200
#     distance_fee = distance_km * 50

#     # Speed multiplier
#     speed_multiplier = 1.0 if speed == "standard" else 1.5

#     # Package type surcharge
#     package_surcharge = 0
#     if package_type == "fragile":
#         package_surcharge = 500
#     elif package_type == "oversized":
#         package_surcharge = 1000

#     total_price = (base_fee + weight_fee + distance_fee + package_surcharge) * speed_multiplier

#     return round(total_price, 2)

