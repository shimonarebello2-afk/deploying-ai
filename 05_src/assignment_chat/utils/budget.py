
from langchain_core.tools import tool


@tool
def calculate_travel_budget(
    flight_cost: float,
    accommodation_cost: float,
    food_cost: float,
    activities_cost: float,
    transport_cost: float
) -> str:
    """
    Calculate the total cost of a trip.

    All costs should be provided in the same currency.
    """

    total = (
        flight_cost
        + accommodation_cost
        + food_cost
        + activities_cost
        + transport_cost
    )

    return (
        f"Your estimated travel budget is {total:.2f}. "
        f"This includes flights, accommodation, food, activities, "
        f"and local transportation."
    )
