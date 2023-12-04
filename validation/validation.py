"""
Also need to validate that if longitude is filled in, lat is as well, and vise-versa...
"""


def validate_iata(value):
    if len(value) != 3:
        return False
    if not validate_is_alpha(value):
        return False
    else:
        return True


def validate_icao(value):
    if len(value) != 4:
        return False
    if not validate_is_alpha(value):
        return False
    else:
        return True


def validate_is_alpha(value):
    """
    validates whether a given value contains only letters
    :param value: value to test
    :return: true if contains only letters, false if not
    """
    if value.isalpha():
        return True
    else:
        return False


def is_float(value):
    """
    determines if a user's input is a float
    :param value: the value to evaluate
    :return: true if the value is a float, false if not
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_positive_int(value):
    """
    determines if a value is a positive integer
    :param value: value to test
    :return: true if value is a positive integer, false if not
    """
    try:
        int(value)
    except ValueError:
        return False
    if int(value) >= 0:
        return True
    else:
        return False


def validate_utc(value):
    # check to make sure it's a number (is_float will work best since it can be negative)
    if not is_float(value):
        return False
    # this min/max value is from wikipedia
    if -12 <= int(value) <= 14:
        return True
    else:
        return False

