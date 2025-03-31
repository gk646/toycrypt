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


#  SPDX-License-Identifier: GPL-3.0-only


# Division with rest
def modulo(a: int, b: int) -> [int, int]:
    """Returns q and r such that a = q * b + r or r = a mod b. Performs division with rest. b must be >0"""
    if b == 0:
        return [None, None]
    q = round_down(float(a) / float(b))  # q = [a/b]
    r = a - b * q
    return [q, r]


# Greatest common divisor
def gcd(a: int, b: int) -> int:
    """Returns the greatest common divisor (gcd) of a and b. It is the greatest number that divides both a and b"""
    if a == 0 and b == 0:  # Rule
        return 0
    if b == 0:
        return abs(a)  # gcd is always positive
    q, r = modulo(a, b)
    return gcd(b, r)


# Euclidean Algorithm
def gcd_ex(a: int, b: int) -> [int, [int]]:
    """Returns the gcd and the list of quotients. Uses the Euclidean algorithm """
    if a == 0 and b == 0:  # Rule
        return 0
    quotients = []
    curr_a = a
    curr_b = b
    while True:
        q, r = modulo(curr_a, curr_b)
        quotients.append(q)
        if r == 0:
            break
        curr_a = curr_b
        curr_b = r
    return curr_b, quotients


def lcm(a: int, b: int) -> int:
    """Returns the least common multiple (lcm) of a and b."""
    return int((a * b) / gcd(a, b))  # Because gcd(a,b) * lcm(a,b) = a * b holds


def linear_combination_solvable(a: int, b: int, n: int) -> bool:
    greatest_common_divisor = gcd(a, b)
    return is_divider(n, greatest_common_divisor)


class Matrix2x2:
    a11: int
    a12: int
    a21: int
    a22: int

    def __init__(self, a11: int, a12: int, a21: int, a22: int):
        self.a11 = a11
        self.a12 = a12
        self.a21 = a21
        self.a22 = a22

    def __mul__(self, b: "Matrix2x2"):
        result: Matrix2x2 = Matrix2x2(0, 0, 0, 0)

        result.a11 = self.a11 * b.a11 + self.a12 * b.a21
        result.a12 = self.a11 * b.a21 + self.a12 * b.a22
        result.a21 = self.a21 * b.a11 + self.a22 * b.a12
        result.a22 = self.a21 * b.a21 + self.a22 * b.a22

        return result

    def __str__(self):
        return (f"[[{self.a11},{self.a12}]\n"
                f"[{self.a21},{self.a22}]]")

    @staticmethod
    def identity():
        return Matrix2x2(1, 0, 0, 1)

    @staticmethod
    def euclideanQ(q: int):
        return Matrix2x2(q, 1, 1, 0)


# Extended Euclidean Algorithm
def eec(a: int, b: int) -> [int, int]:
    """Returns the coefficients x and y such that the linear combination gcd(a,b) = a*x + b*y holds"""
    divisor, quotients = gcd_ex(a, b)
    result: Matrix2x2 = Matrix2x2.euclideanQ(quotients[0])
    for i in range(1, len(quotients)):
        result = result * Matrix2x2.euclideanQ(quotients[i])

    x = pow(-1, len(quotients)) * result.a22
    y = pow(-1, len(quotients) - 1) * result.a12

    return x, y

