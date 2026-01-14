from emission_factors import FACTORS


def calculate_emissions(form_data):
    """
    Computes carbon emissions based on SCAR form inputs.

    Parameters
    ----------
    form_data : dict
        Dictionary obtained from request.form.to_dict()
        (all values are received as strings)

    Returns
    -------
    emissions : dict
        Dictionary {activity_category: emissions_in_kgCO2e}
        containing only categories with emissions > 0
    total : float
        Total carbon emissions (kgCO2e)
    """

    # Dictionary storing emissions per activity category
    emissions = {}

    # Total emissions accumulator
    total = 0.0

    # Loop over all emission factors defined in the FACTORS dictionary
    for key, factor in FACTORS.items():

        # Safely retrieve the user-provided value for the given activity
        raw_value = form_data.get(key, 0)

        try:
            # Convert input value to float
            activity_value = float(raw_value)
        except (ValueError, TypeError):
            # If conversion fails, default to zero
            activity_value = 0.0

        # Prevent negative values
        if activity_value < 0:
            activity_value = 0.0

        # Compute emissions for the activity
        emission_value = activity_value * factor

        # Keep only meaningful (non-zero) emission categories
        if emission_value > 0:
            emission_value = round(emission_value, 2)
            emissions[key] = emission_value
            total += emission_value

    # Return both the detailed emissions and the aggregated total
    return emissions, total

