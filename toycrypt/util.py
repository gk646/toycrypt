#  SPDX-License-Identifier: GPL-3.0-only

import time
import toymath


def xor(a: int, b: int) -> int:
    """
    Returns the result of the XOR operation applied to every bit of both numbers
    XOR returns 1 if and only if either input is 1:
    0 1 => 1
    1 0 => 1
    0 0 => 0
    1 1 => 0
    :param a: a number
    :param b: a second number
    :return: the result of the xor operation applied to every bit
    """
    return a ^ b


def measure(function, *args, **kwargs):
    """
    Measures the time it takes to complete the given method with the given arguments
    :param function: any function that is called
    :param args: function arguments in correct order
    :param kwargs: keyword arguments that can be in any order (e.g. input1="Hello")
    :return: result of the function call
    """
    start_time = time.time()
    result = function(*args, **kwargs)
    end_time = time.time()
    print(f"Took {end_time - start_time}")
    return result


def geometric_progression(b: int, sequence: str) -> int:
    """Returns the numeric value of the sequence with the given base b. Only works for 1 <= g < 36"""
    if b == 0:
        return 1
    k = len(sequence)
    result: int = 0
    for i, c in enumerate(sequence, 1):
        a = int(c, b)
        if a > b or a >= 26:
            raise ValueError
        result += a * pow(b, k - i)
    return result


def geometric_progression_rev(b: int, number: int) -> str:
    """Returns string representation of the number in the given base b. Only works for 1 <= g < 36"""
    if b == 0:
        raise ValueError

    if number == 0:
        return "0"

    result: str = ""

    if b == 1:
        for i in range(number):
            result += "1"
        return result

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"

    while number > 0:
        q, r = toymath.modulo(number, b)
        result += digits[r]
        number //= b
    return ''.join(reversed(result))


def binary2decimal(binary: str) -> int:
    return geometric_progression(2, binary)


def decimal2binary(decimal: int) -> str:
    return geometric_progression_rev(2, decimal)


def hex2decimal(hexa: str) -> int:
    return geometric_progression(16, hexa)


def decimal2hex(decimal: int) -> str:
    return geometric_progression_rev(16, decimal)
