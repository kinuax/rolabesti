from datetime import datetime


def length_to_string(length: int) -> str:
    """Return the string representation of length."""
    length_format = "%M:%S" if length < 3600 else "%H:%M:%S"
    return datetime.fromtimestamp(length).strftime(length_format)
