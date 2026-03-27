from quotes.models import Quote


from quotes.models import Quote


def get_quantity_score(quantity):
    if quantity <= 10:
        return 1
    elif quantity <= 50:
        return 2
    elif quantity <= 100:
        return 3
    return 4


def get_size_score(size):
    if size == Quote.SMALL:
        return 1
    elif size == Quote.MEDIUM_SIZE:
        return 2
    elif size == Quote.LARGE:
        return 3
    return 0


def get_urgency_score(urgency):
    if urgency == Quote.LOW:
        return 1
    elif urgency == Quote.MEDIUM:
        return 2
    elif urgency == Quote.HIGH:
        return 3
    return 0


def get_installation_score(installation_required):
    return 2 if installation_required else 0


def get_customer_category_score(customer_category):
    if customer_category == Quote.REGULAR:
        return 1
    elif customer_category == Quote.CORPORATE:
        return 2
    elif customer_category == Quote.VIP:
        return 3
    return 0


def calculate_total_score(quote):
    service_score = quote.service_type.base_complexity_score if quote.service_type else 0
    material_score = quote.material.complexity_score if quote.material else 0

    total_score = (
        service_score
        + material_score
        + get_quantity_score(quote.quantity)
        + get_size_score(quote.size)
        + get_urgency_score(quote.urgency)
        + get_installation_score(quote.installation_required)
        + get_customer_category_score(quote.customer_category)
    )

    return total_score