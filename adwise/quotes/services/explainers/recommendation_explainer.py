def build_recommendation_explanation(quote, total_score, data, is_preliminary=False):

    explanation = (
        "This recommendation is generated based on predefined scoring rules "
    "applied to the selected job parameters. \nFinal decision remains with the admin."
    )

    if is_preliminary:
        explanation += "\nAdditional caution is required due to unknown inputs."

    return explanation