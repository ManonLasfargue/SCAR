"""
SCAR scenario module.

This module provides a high-level interface to all scenario
generation functions implemented in SCAR.

It centralises access to scenario logic and exposes only the
public functions intended to be used by the rest of the application.
"""

from .engine import (
    scenario_modal_substitution,
    scenario_digital_sobriety,
    scenario_utility_aware,
)

# Explicitly define the public API of the scenario module.
# Only the listed functions will be accessible when using
# 'from scenarios import *'.
__all__ = [
    "scenario_modal_substitution",
    "scenario_digital_sobriety",
    "scenario_utility_aware",
]
