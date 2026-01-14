# calculations/categories.py

# ==========================================
# Emission post → category mapping
# ==========================================

EMISSION_CATEGORIES = {

    # -------- MOBILITY --------
    "flight_short": "Mobility",
    "flight_medium": "Mobility",
    "flight_long": "Mobility",
    "train_tgv": "Mobility",
    "train_ter": "Mobility",
    "car_diesel": "Mobility",
    "car_essence": "Mobility",
    "carpool": "Mobility",
    "bus": "Mobility",
    "metro": "Mobility",

    # -------- ENERGY --------
    "electricity": "Energy",
    "gas": "Energy",
    "fioul": "Energy",
    "heating_network": "Energy",

    # -------- DIGITAL --------
    "laptops": "Digital",
    "desktop": "Digital",
    "screen": "Digital",
    "server": "Digital",
    "cloud": "Digital",
    "video_conf": "Digital",
    "email": "Digital",
    "llm_usage": "Digital",
    "ai_training": "Digital",

    # -------- FOOD --------
    "meat_meals": "Food",
    "white_meat_meals": "Food",
    "veg_meals": "Food",
    "coffee": "Food",

    # -------- EVENTS --------
    "hotel_night": "Events & Accommodation",
    "airbnb_night": "Events & Accommodation",
    "conference_day": "Events & Accommodation",
    "conference_meal": "Events & Accommodation",
}


def aggregate_by_category(emissions_by_post):
    """
    Aggregate emissions from individual posts into higher-level categories.

    Parameters
    ----------
    emissions_by_post : dict
        Emissions by post (kgCO2e).

    Returns
    -------
    dict
        Emissions aggregated by category (kgCO2e).
    """
    categories = {}

    for post, value in emissions_by_post.items():
        if value <= 0:
            continue

        category = EMISSION_CATEGORIES.get(post, "Other")
        categories[category] = categories.get(category, 0) + value

    return {k: round(v, 2) for k, v in categories.items()}
