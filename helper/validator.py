import re

from marshmallow import ValidationError


def is_valid_number(number) -> bool:
    if number < 0:
        raise ValidationError("Number in this field cannot be negative!")
    if number > 2 ** 63 - 1:
        raise ValidationError("Number in this field is out of range!")
    return True


def is_valid_subdomain(subdomain: str) -> bool:
    pattern = "[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])"
    return bool(re.match(pattern, subdomain))
