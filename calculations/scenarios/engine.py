"""
SCAR – Scenario engine

This module implements the core logic of scenario construction in SCAR.
Each function takes a baseline emission profile and returns a modified
(emissions) dictionary representing a counterfactual scenario.
"""

from .rules import (
    DIGITAL_SOBRIETY_POSTS,
    MAX_DIGITAL_REDUCTION,
    MAX_FLIGHT_SUBSTITUTION,
    CAR_SUBSTITUTION_RATE,
    UTILITY_SCENARIO_LEVELS,
)

from .utils import copy_emissions


def scenario_modal_substitution(baseline: dict) -> dict:
    """
    Modal substitution scenario.

    This scenario simulates partial substitution of high-carbon mobility modes
    (flights and individual car use) with lower-carbon alternatives.
    Travel demand is kept constant; only transport modes are adjusted.
    """

    # Create a safe copy of baseline emissions to avoid mutating input data
    emissions = copy_emissions(baseline)

    # Apply substitution rules for flights depending on distance category
    for flight, max_rate in MAX_FLIGHT_SUBSTITUTION.items():
        if flight in emissions and emissions[flight] > 0:

            # Compute the reducible share of flight emissions
            reduced = emissions[flight] * max_rate

            # Reduce flight emissions accordingly
            emissions[flight] -= reduced

            # Reallocate a small fraction of reduced emissions to rail travel
            # (to reflect lower-carbon but non-zero alternatives)
            emissions["train_tgv"] = emissions.get("train_tgv", 0) + reduced * 0.1

    # Apply substitution rules for individual car use
    for car in {"car_diesel", "car_essence"}:
        if car in emissions and emissions[car] > 0:

            # Compute emissions shifted from individual car use
            reduced = emissions[car] * CAR_SUBSTITUTION_RATE

            # Reduce car emissions
            emissions[car] -= reduced

            # Reallocate emissions to carpooling
            emissions["carpool"] = emissions.get("carpool", 0) + reduced

    return emissions


def scenario_digital_sobriety(baseline: dict) -> dict:
    """
    Digital sobriety scenario.

    This scenario simulates moderate reductions in emissions associated with
    digital practices that are considered adjustable through organisational
    or behavioural changes (e.g. cloud usage, videoconferencing, email volume).
    """

    # Copy baseline emissions
    emissions = copy_emissions(baseline)

    # Apply a uniform proportional reduction to digital sobriety posts
    for post in DIGITAL_SOBRIETY_POSTS:
        if post in emissions and emissions[post] > 0:
            emissions[post] *= (1 - MAX_DIGITAL_REDUCTION)

    return emissions


def scenario_utility_aware(baseline: dict, utility: int) -> dict:
    """
    Utility-aware scenario.

    This scenario modulates emission reductions based on the perceived
    scientific or societal usefulness of the project. Higher utility leads
    to more conservative reductions, while lower utility allows stronger
    proportional adjustments.
    """

    # Copy baseline emissions
    emissions = copy_emissions(baseline)

    # Define reduction parameters depending on utility score
    if utility >= 8:
        digital_reduction = 0.1
        mobility_factor = 0.5
    elif utility >= 5:
        digital_reduction = 0.25
        mobility_factor = 1.0
    else:
        digital_reduction = 0.4
        mobility_factor = 1.3

    # Apply utility-dependent reductions to digital sobriety posts
    for post in DIGITAL_SOBRIETY_POSTS:
        if post in emissions and emissions[post] > 0:
            emissions[post] *= (1 - digital_reduction)

    # Apply utility-dependent adjustments to flight emissions
    for flight, max_rate in MAX_FLIGHT_SUBSTITUTION.items():
        if flight in emissions and emissions[flight] > 0:

            # Compute reducible emissions, capped by maximum substitution rate
            reduced = emissions[flight] * min(max_rate * mobility_factor, max_rate)

            # Reduce flight emissions
            emissions[flight] -= reduced

            # Reallocate a fraction to rail travel
            emissions["train_tgv"] = emissions.get("train_tgv", 0) + reduced * 0.1

    # Apply utility-dependent adjustments to individual car use
    for car in {"car_diesel", "car_essence"}:
        if car in emissions and emissions[car] > 0:

            # Compute reduced emissions from car travel
            reduced = emissions[car] * CAR_SUBSTITUTION_RATE * mobility_factor

            # Reduce car emissions
            emissions[car] -= reduced

            # Reallocate emissions to carpooling
            emissions["carpool"] = emissions.get("carpool", 0) + reduced

    return emissions
