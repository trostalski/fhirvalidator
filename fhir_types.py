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
