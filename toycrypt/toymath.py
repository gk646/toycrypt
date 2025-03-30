def round_down(num: float) -> float:
    """Returns the greatest whole number, smaller or equal to num
     Gaussian square bracket; [num]
     """
    whole: int = int(num)
    if whole > num:
        return whole - 1
    return whole


def is_divider(n: int, a: int) -> bool:
    """Checks if a divides n. This means n is dividable by a. Uses naive approach"""
    if n == 0:
        return True
    if a == 0:  # if a == 0 then 0 * b = n only holds for n == 0 as any b multiplied with 0 must be 0 (in real numbers)
        return n == 0
    if a > n:
        return False

    # A number n is dividable if there is any factor b such that a * b = n
    for i in range(n):
        if i * a == n:  # Check positive multiplier
            return True
        elif -i * a == n:  # Check negative multiplier
            return True
    return False


# Division with rest

def modulo(a: int, b: int) -> [int, int]:
    """Returns q and r such that a = q * b + r or r = a mod b. Performs division with rest. b must be >0"""
    if b == 0:
        return [None, None]
    q = round_down(float(a) / float(b))  # q = [a/b]
    r = a - b * q
    return [q, r]

# Greatest common divisor

def gcd(a : int, b : int) -> int:
    if a == 0 or b == 0:
        return  0
