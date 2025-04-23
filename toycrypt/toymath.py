#  SPDX-License-Identifier: GPL-3.0-only
import math


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
    n = abs(n)
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
def modulo(a: int, n: int) -> [int, int]:
    """Returns q and r such that a = q * n + r or r = a mod n. Performs division with rest. n must be >0"""
    if n == 0:
        return [None, None]
    q = round_down(float(a) / float(n))  # q = [a/n]
    r = a - n * q
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


def get_least_positive_residue(a: int, n: int) -> int:
    """Returns the least positive element in the same residue as the given a in modulo n"""
    a = abs(a)  # Make it positive
    q, r = modulo(a, n)  # Make it smaller than n
    return n - r  # Returns the least positive element


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
    def eec_Q(q: int):
        return Matrix2x2(q, 1, 1, 0)


# Extended Euclidean Algorithm
def eec(a: int, b: int) -> [int, int]:
    """Returns the coefficients x and y such that the linear combination gcd(a,b) = a*x + b*y holds"""
    divisor, quotients = gcd_ex(a, b)
    result: Matrix2x2 = Matrix2x2.eec_Q(quotients[0])
    for i in range(1, len(quotients)):
        result = result * Matrix2x2.eec_Q(quotients[i])

    x = pow(-1, len(quotients)) * result.a22
    y = pow(-1, len(quotients) - 1) * result.a12

    return x, y


def is_modulo_congruent(a: int, b: int, n: int) -> bool:
    """Returns boolean if a and b are in the same residue when modulo n. Only works for n >= 2"""
    if n < 2:
        return False
    # Alternative: congruence holds if n divides a - b
    # return is_divider(a - b, n)

    # Naive approach just compare the rest
    aq, ar = modulo(a, n)
    bq, br = modulo(b, n)
    return ar == br


def table_to_str(table: [[int]], mode="add") -> str:
    """
    Returns a printable string of the given table.
    :param mode either add or mult"""
    if mode == "add":
        ret = "|+|"
    elif mode == "mult":
        ret = "|*|"
    else:
        raise ValueError("Invalid mode")

    n: int = len(table)
    for i in range(n):
        ret += f"|{i}"
    ret += "|\n"

    for i in range(n):
        ret += f"|{i}|"
        for j in range(n):
            ret += f" {table[i][j]}"
        ret += "|\n"
    return ret


def get_add_table(n: int) -> [[int]]:
    """Returns a numeric table of the addition table of the given n."""
    ret: [[int]] = []
    for i in range(n):
        ret.append([])
        for j in range(n):
            ret[i].append(modulo(i + j, n)[1])
    return ret


def get_mult_table(n: int) -> [[int]]:
    """Returns a numeric table of the addition table of the given n."""
    ret: [[int]] = []
    for i in range(n):
        ret.append([])
        for j in range(n):
            ret[i].append(modulo(i * j, n)[1])
    return ret


def has_mult_inverse(a: int, n: int) -> bool:
    """Returns true if, given a number a ∈ {1,...,n-1} and a modulo n,
    there exists a multiplicative inverse a-1 such that a * a-1 congruent 1 mod n.
    This holds if a and n are co-prime to each other. """
    return gcd(a, n) == 1


def get_multi_inverse(a: int, n: int) -> int:
    if not has_mult_inverse(a, n):
        raise ValueError("a is not co-prime to n")
    fa, fb = eec(n, a)
    return get_least_positive_residue(fb, n)


def pow_naive(x: int, y: int) -> int:
    """Returns x to the power of y"""
    if y == 0:
        return 1
    if y < 0:
        raise ValueError("Only positive exponents")
    ret = 1
    # This approach takes y many multiplications
    # Thus has complexity O(n)
    for i in range(y):
        ret *= x
    return ret


def pow_mult_sqr(x: int, y: int) -> int:
    if y == 0:
        return 1
    if y < 0:
        raise ValueError("Only positive exponents")
    result: int = 1
    base = x
    exp = y
    # This approach uses at most 2 * log2(y) multiplications
    # Thus has complexity O(log2(n))
    while exp > 0:
        if exp & 1:
            result *= base
        base *= base
        exp >>= 1
    return result


def get_residue_set(n: int) -> [int]:
    """Returns the residue set of the given modulo n. {0, ..., n-1}"""
    return [i for i in range(n)]


def get_reduced_residue_set(n: int) -> [int]:
    """Returns the reduced residue set of the given modulo n, such that all elements are co-prime to n."""
    ret: [int] = []
    for i in range(n):
        if gcd(i, n) == 1:
            ret.append(i)
    return ret


def euler_phi(n: int) -> int:
    """Applies the euler phi function to n."""
    ret: int = 0
    for i in range(n):
        if gcd(i, n) == 1:
            ret += 1
    return ret


def little_fermat(a: int, p: int) -> bool:
    """Returns true if for a given a and p, a**(p1) congruent to 1 mod p holds. """
    if euler_phi(p) != p - 1 or gcd(a, p) != 1:
        return False  # p is not a prime or a is not co-prime to p
    return pow(a, p - 1, p) == 1


def euler_fermat(residue: [int], n: int) -> bool:
    """Returns true if the given residue set is a reduced set and satisfies the euler-fermat theorem: all members are co-prime to n, and a**phi(n) congruent to 1 mod n holds."""
    phi = euler_phi(n)
    for a in residue:
        if gcd(a, n) != 1:
            return False
        if pow(a, phi, n) != 0:
            return False
    return True


