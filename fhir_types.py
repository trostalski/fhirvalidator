import re


def is_base64Binary(value: str) -> bool:
    pattern = r"(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?"
    return bool(re.fullmatch(pattern, value))


def is_boolean(value: str) -> bool:
    return value in ["true", "false"]


def is_canonical(value: str) -> bool:
    pattern = r"\S*"
    return bool(re.fullmatch(pattern, value))


def is_code(value: str) -> bool:
    pattern = r"[^\s]+( [^\s]+)*"
    return bool(re.fullmatch(pattern, value))


def is_date(value: str) -> bool:
    pattern = r"([0-9]{4}(-[0-9]{2}(-[0-9]{2})?)?)?"
    return bool(re.fullmatch(pattern, value))


def is_dateTime(value: str) -> bool:
    pattern = r"([0-9]{4}(-[0-9]{2}(-[0-9]{2}(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]{1,9})?)?)?)?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)?)?)?"
    return bool(re.fullmatch(pattern, value))


def is_decimal(value: str) -> bool:
    pattern = r"-?(0|[1-9][0-9]{0,17})(\.[0-9]{1,17})?([eE][+-]?[0-9]{1,9})?"
    return bool(re.fullmatch(pattern, value))


def is_id(value: str) -> bool:
    pattern = r"[A-Za-z0-9\-\.]{1,64}"
    return bool(re.fullmatch(pattern, value))


def is_instant(value: str) -> bool:
    pattern = r"([0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]{1,9})?(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))"
    return bool(re.fullmatch(pattern, value))


def is_integer(value: str) -> bool:
    pattern = r"[0]|[-+]?[1-9][0-9]*"
    return bool(re.fullmatch(pattern, value))


def is_integer64(value: str) -> bool:
    pattern = r"[0]|[-+]?[1-9][0-9]*"
    return bool(re.fullmatch(pattern, value))


def is_markdown(value: str) -> bool:
    pattern = r"^[\s\S]+$"
    return bool(re.fullmatch(pattern, value))


def is_oid(value: str) -> bool:
    pattern = r"urn:oid:[0-2](\.(0|[1-9][0-9]*))+"
    return bool(re.fullmatch(pattern, value))


def is_string(value: str) -> bool:
    return isinstance(value, str) and len(value) <= 1048576


def is_positiveInt(value: str) -> bool:
    pattern = r"[1-9][0-9]*"
    return bool(re.fullmatch(pattern, value))


def is_time(value: str) -> bool:
    pattern = r"([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]{1,9})?"
    return bool(re.fullmatch(pattern, value))


def is_unsignedInt(value: str) -> bool:
    pattern = r"[0]|([1-9][0-9]*)"
    return bool(re.fullmatch(pattern, value))


def is_uri(value: str) -> bool:
    pattern = r"\S*"
    return bool(re.fullmatch(pattern, value))


def is_url(value: str) -> bool:
    pattern = r"\S*"
    return bool(re.fullmatch(pattern, value))


def is_uuid(value: str) -> bool:
    pattern = r"urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    return bool(re.fullmatch(pattern, value))


def check_primitive_fhir_type(fhir_type: str, value):
    if fhir_type == "base64Binary":
        return is_base64Binary(value)
    elif fhir_type == "boolean":
        return is_boolean(value)
    elif fhir_type == "canonical":
        return is_canonical(value)
    elif fhir_type == "code":
        return is_code(value)
    elif fhir_type == "date":
        return is_date(value)
    elif fhir_type == "dateTime":
        return is_dateTime(value)
    elif fhir_type == "decimal":
        return is_decimal(value)
    elif fhir_type == "id":
        return is_id(value)
    elif fhir_type == "instant":
        return is_instant(value)
    elif fhir_type == "integer":
        return is_integer(value)
    elif fhir_type == "integer64":
        return is_integer64(value)
    elif fhir_type == "markdown":
        return is_markdown(value)
    elif fhir_type == "oid":
        return is_oid(value)
    elif fhir_type == "positiveInt":
        return is_positiveInt(value)
    elif fhir_type == "string" or fhir_type == "http://hl7.org/fhirpath/System.String":
        return is_string(value)
    elif fhir_type == "time":
        return is_time(value)
    elif fhir_type == "unsignedInt":
        return is_unsignedInt(value)
    elif fhir_type == "uri":
        return is_uri(value)
    elif fhir_type == "url":
        return is_url(value)
    elif fhir_type == "uuid":
        return is_uuid(value)
    elif fhir_type == "xhtml":
        return True
    else:
        raise ValueError(f"Unknown FHIR type: {fhir_type}")
