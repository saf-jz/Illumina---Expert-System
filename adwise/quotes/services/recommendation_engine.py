from quotes.models import SystemRecommendation
from quotes.services.classifiers.input_classifier import has_unknown_inputs
from quotes.services.rules.scoring_rules import calculate_total_score
from quotes.services.rules.recommendation_rules import map_score_to_recommendation
from quotes.services.explainers.recommendation_explainer import build_recommendation_explanation


def generate_recommendation_data(quote):
    total_score = calculate_total_score(quote)
    data = map_score_to_recommendation(total_score)

    unknown = has_unknown_inputs(quote.service_type, quote.material)

    recommendation_type = (
        SystemRecommendation.PRELIMINARY_RECOMMENDATION
        if unknown
        else SystemRecommendation.SYSTEM_RECOMMENDATION
    )

    if unknown:
        data["approval_recommendation"] = "Admin Review Required"

    explanation = build_recommendation_explanation(
        quote=quote,
        total_score=total_score,
        data=data,
        is_preliminary=unknown,
    )

    return {
        "system_price_tier": data["price_tier"],
        "system_margin_range": data["margin_range"],
        "system_approval_recommendation": data["approval_recommendation"],
        "system_explanation": explanation,
        "recommendation_type": recommendation_type,
        "total_score": total_score,
    }


def generate_and_save_recommendation(quote):
    recommendation_data = generate_recommendation_data(quote)

    recommendation, created = SystemRecommendation.objects.update_or_create(
        quote=quote,
        defaults=recommendation_data,
    )

    return recommendation