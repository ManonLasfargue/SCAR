"""
SCAR – Scenario rules

This module defines the conceptual and methodological rules
governing scenario construction in SCAR.

It specifies:
- which emission categories can be modified,
- under which constraints,
- and with which maximum reduction limits.

No numerical calculations are performed here.
This file serves as a rule-based configuration layer
used by scenario functions.
"""

# =========================
# POST CLASSIFICATION
# =========================

# Emission categories considered structurally constrained
# (typically difficult to modify at the project level)
STRUCTURAL_POSTS = {
    "electricity",
    "gas",
    "fioul",
    "heating_network",
}

# Emission categories that can only be weakly adjusted
# (often linked to collective or institutional settings)
WEAKLY_SCENARISABLE_POSTS = {
    "hotel_night",
    "airbnb_night",
    "conference_day",
    "conference_meal",
}

# Mobility-related emission categories that can potentially
# be substituted with lower-carbon transport modes
MOBILITY_SUBSTITUTION_POSTS = {
    "flight_short",
    "flight_medium",
    "flight_long",
    "car_diesel",
    "car_essence",
}

# Lower-carbon mobility alternatives used in substitution scenarios
MOBILITY_ALTERNATIVES = {
    "train_tgv",
    "train_ter",
    "carpool",
    "bus",
    "metro",
}

# Digital activities that can be reduced through
# digital sobriety practices (behavioural or organisational)
DIGITAL_SOBRIETY_POSTS = {
    "cloud",
    "video_conf",
    "email",
    "llm_usage",
}

# Digital emission categories considered structurally embedded
# (hardware, infrastructure, or heavy computation)
DIGITAL_STRUCTURAL_POSTS = {
    "server",
    "ai_training",
    "laptops",
    "desktop",
    "screen",
}

# =========================
# SCENARIO PARAMETERS
# =========================

# Maximum share of flights that can be substituted
# depending on flight distance category
MAX_FLIGHT_SUBSTITUTION = {
    "flight_short": 0.6,    # up to 60% substitution
    "flight_medium": 0.4,  # up to 40% substitution
    "flight_long": 0.15,   # up to 15% substitution
}

# Share of car travel that can be substituted
# (e.g. through carpooling or alternative modes)
CAR_SUBSTITUTION_RATE = 0.3

# Maximum proportional reduction allowed for digital activities
MAX_DIGITAL_REDUCTION = 0.3  # 30%

# Utility score thresholds used to classify projects
UTILITY_HIGH = 8
UTILITY_MEDIUM = 5

# Global cap on total emission reductions
# to avoid unrealistic or excessive scenario outcomes
MAX_GLOBAL_REDUCTION = 0.2  # 20%

# =========================
# UTILITY-AWARE PARAMETERS
# =========================

# Definition of scenario parameters based on project utility level
# Higher utility implies more conservative reductions,
# lower utility allows stronger proportional adjustments
UTILITY_SCENARIO_LEVELS = {
    "high": {
        "min_utility": 8,
        "digital_reduction": 0.10,
        "mobility_reduction_factor": 0.5,
    },
    "medium": {
        "min_utility": 5,
        "digital_reduction": 0.25,
        "mobility_reduction_factor": 1.0,
    },
    "low": {
        "min_utility": 0,
        "digital_reduction": 0.40,
        "mobility_reduction_factor": 1.3,
    },
}

