

def is_int(int_check):
    try:
        number = int(int_check)
        return number
    except ValueError:
        return None
    except OverflowError:
        return None
