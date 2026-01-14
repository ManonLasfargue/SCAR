"""
Utility functions for scenario calculations.

This module provides small helper functions used across
scenario computations in SCAR. These functions are generic,
side-effect free, and independent of specific scenario logic.
"""


def copy_emissions(emissions: dict) -> dict:
    """
    Return a safe copy of an emissions dictionary.

    This function creates a new dictionary where all values
    are explicitly converted to floats. It is used to avoid
    mutating the original emissions data when constructing
    counterfactual scenarios.
    """
    return {k: float(v) for k, v in emissions.items()}


def total_emissions(emissions: dict) -> float:
    """
    Compute the total amount of emissions.

    This function aggregates all emission values contained
    in the dictionary and returns their sum, expressed in kgCO₂e.
    """
    return sum(emissions.values())


def relative_share(emissions: dict, keys: set) -> float:
    """
    Compute the relative share of selected emission categories.

    Parameters
    ----------
    emissions : dict
        Dictionary of emissions by category.
    keys : set
        Set of emission categories whose combined share is evaluated.

    Returns
    -------
    float
        Proportion of total emissions represented by the selected categories.
        Returns 0.0 if total emissions are equal to zero.
    """

    # Compute total emissions to normalise the share
    total = total_emissions(emissions)

    # Avoid division by zero
    if total == 0:
        return 0.0

    # Sum emissions for selected categories and normalise
    return sum(emissions.get(k, 0) for k in keys) / total
