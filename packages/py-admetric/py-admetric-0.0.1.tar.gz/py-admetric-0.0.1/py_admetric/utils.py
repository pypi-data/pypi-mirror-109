def safe_div(numerator: int, denominator: int) -> float:
    """Divide without Zero Division Error.

    Args:
        numerator (integer): the number above the line in a vulgar fraction.
        denominator (integer): the number below the line in a vulgar fraction.
    Returns:
        float: Return value
    Usage:
      >>> from py_admetric import utils
      >>> val = utils.safe_div(1,1)
    """

    if denominator == 0:
        return 0.0
    return numerator / denominator


def validate_negative(a: int, b: int):
    """Raise error if any of args are less than 0.

    Args:
        a (integer): args1
        b (integer): args2
    Raises:
        ValueError: if either a or b is less than 0
    Usage:
        >>> from py_admetric import utils
        >>> val = utils.validate_negative(-1, -1)
    """

    if a < 0 or b < 0:
        raise ValueError(f"values must be positive, denominator={a}, numerator={b}")


def validate_integer(a: any, b: any):
    """Raise error if any of args are not integer.

    Args:
        a (any): args1
        b (any): args2
    Raises:
        ValueError: if either a or b is not integer
    Usage:
        >>> from py_admetric import utils
        >>> val = utils.validate_integer(1.22, 2.31)
    """

    if not(isinstance(a, int) and isinstance(b, int)):
        raise ValueError(f"both of values must be integer, denominator={a}, numerator={b}")
