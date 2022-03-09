from utils.string import valid_phone


def phone_number(value: str) -> str:
    assert valid_phone(value), "Not a valid phone number"
    return value


def letters_or_spaces(value: str) -> str:
    assert all(c.isalpha() or c.isspace() for c in value), "Not a valid name, only letters or spaces allowed"
    return value
