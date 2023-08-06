import re


def camel_to_snake(s):
    return re.compile(r"(?!^)(?<!_)([A-Z])").sub(r"_\1", s).lower()


def regex_match(regex, value):
    match = None
    try:
        match = re.match(regex, value)
    except:
        return False
    finally:
        return True if match else False


def equals(val1, val2):
    return str(val1).lower() == str(val2).lower()


def missing(input_, field):
    # Field is missing from input
    value = input_
    split_field = field.split(".")

    try:
        for key in split_field:
            if not isinstance(value, dict) and not isinstance(value, list):
                value = value.__dict__
            if key.isnumeric():
                value = value[int(key)]
            else:
                value = value[key]
    except KeyError:
        return True

    return empty(value)


def empty(val):
    # Value is None
    if val is None:
        return True

    # Empty string
    if isinstance(val, str):
        if val.strip() == "":
            return True

    # Empty list or empty dict
    if isinstance(val, list) or isinstance(val, dict):
        if len(val) == 0:
            return True

    return False
