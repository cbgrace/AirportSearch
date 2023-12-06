"""
This module contains various functions to evaluate user entries from the gui layer.

Methods:
--------
    validate_iata(value):
        validates the IATA code from the GUI
    validate_icao(value):
        validates the ICAO code from the GUI
    validate_is_alpha(value):
        validates whether a given value contains only letters
    is_float(value):
        determines if a user's input is a float
    is_positive_int(value):
        determines if a value is a positive integer
    validate_utc(value):
        validates the UTC entry from the gui

Constants:
----------
    IATA_CODE_LENGTH: the length of a IATA code
    ICAO_CODE_LENGTH: the length of a ICAO code
    MINIMUM_UTC: the minimum UTC value
    MAXIMUM_UTC: the maximum UTC value
"""

IATA_CODE_LENGTH = 3
ICAO_CODE_LENGTH = 4
MINIMUM_UTC = -12
MAXIMUM_UTC = 14


def validate_iata(value):
    """
    validates the IATA code from the GUI
    :param value: value to assess
    :return: False if invalid, true if valid
    """
    if len(value) != IATA_CODE_LENGTH:
        return False
    if not validate_is_alpha(value):
        return False
    else:
        return True


def validate_icao(value):
    """
    validates the ICAO code from the GUI
    :param value: value to assess
    :return: True if valid, false if not
    """
    if len(value) != ICAO_CODE_LENGTH:
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
    """
    validates the UTC entry from the gui
    :param value: value to assess
    :return: True if valid, false if not
    """
    # check to make sure it's a number (is_float will work best since it can be negative)
    if not is_float(value):
        return False
    # this min/max value is from wikipedia
    if MINIMUM_UTC <= int(value) <= MAXIMUM_UTC:
        return True
    else:
        return False

