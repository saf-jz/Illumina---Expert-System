def is_unknown_service(service_type):
    if not service_type:
        return True
    return service_type.name.strip().lower() == "unknown / not sure"


def is_unknown_material(material):
    if not material:
        return True
    return material.name.strip().lower() == "unknown / not sure"


def has_unknown_inputs(service_type, material):
    return is_unknown_service(service_type) or is_unknown_material(material)