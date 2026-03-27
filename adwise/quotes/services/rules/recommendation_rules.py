def map_score_to_recommendation(total_score):
    if total_score <= 7:
        return {
            "price_tier": "Basic",
            "margin_range": "10% - 15%",
            "approval_recommendation": "Low Risk - Can Proceed",
        }
    elif total_score <= 12:
        return {
            "price_tier": "Standard",
            "margin_range": "15% - 25%",
            "approval_recommendation": "Normal Review Required",
        }
    else:
        return {
            "price_tier": "Premium",
            "margin_range": "25% - 40%",
            "approval_recommendation": "High Review Required",
        }