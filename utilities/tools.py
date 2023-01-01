

def is_int(int_check):
    """
    determines if a number is an integer

    :param int_check: potential integer
    :return: Integer or None
    """

    try:
        number = int(int_check)
        return number
    except ValueError:
        return None
    except OverflowError:
        return None
