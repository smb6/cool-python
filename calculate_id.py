def is_israeli_id_number(id):
    id = str(id).strip()
    if len(id) > 9 or not id.isdigit():
        return False
    id = id.zfill(9)
    total = 0
    for i, digit in enumerate(id):
        num = int(digit)
        factor = (i % 2) + 1
        step = num * factor
        if step > 9:
            step -= 9
        total += step
    return total % 10 == 0

def calculate_9th_digit(id8):
    """
    Calculate the 9th digit (checksum) for an 8-digit Israeli ID number.

    Parameters:
    id8 (str or int): The first 8 digits of the Israeli ID number.

    Returns:
    str: The 9th digit that makes the full ID number valid.
    """
    id8 = str(id8).strip()
    if len(id8) != 8 or not id8.isdigit():
        raise ValueError("Input must be an 8-digit number.")

    total = 0
    for i, digit in enumerate(id8):
        num = int(digit)
        factor = (i % 2) + 1
        step = num * factor
        if step > 9:
            step -= 9
        total += step

    # Calculate the checksum digit
    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)

if __name__ == '__main__':
    id = '01582749'
    ret = calculate_9th_digit(id)
    full_id = id + ret
    print(ret)
    ret = is_israeli_id_number(full_id)
    print(ret)