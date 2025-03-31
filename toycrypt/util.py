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


def encode16(number: int) -> str:
    """
    Encodes the given number (32 bit) to base16 (hexadecimal) representation
    :param number: any number
    :return: the base16 representation of the input number
    """
    output = ""
    if number < 0 or number > 0xFFFFFFFF:
        raise ValueError("Number must be a 32-bit unsigned integer")

    # The 32-bit number is split into 8 4-bit chunks (that each have a value of 0-16)
    # Then those are transferred to their character representation

    # Transform a number 0-16 into its hexadecimal character
    def num_to_base16(chunk_number: int) -> str:
        if chunk_number < 10:  # 0 - 9 stays the same
            return str(chunk_number)
        return chr(ord('a') + (chunk_number - 10))  # 0-15 become a-f

    # Get the i-th 4 bit chunk from the given number
    def get_4bit_chunk(num: int, index: int) -> int:
        return (num >> (28 - index * 4)) & 0b1111  # Zero all bits except the first 4

    # Process all the 4 bit chunks (8*4 = 32)
    for i in range(8):
        chunk_number = get_4bit_chunk(number, i)
        output += num_to_base16(chunk_number)
    return output


def decode16(base16_string: str) -> int:
    """
    Decodes a given base16 string into its number representation
    :param base16_string: the base16 representation of a number
    :return: the number representation of the base16 string
    """
    output = 0
    # Length must be 8 as we only work with 32-bit numbers - 32/4 = 8
    if len(base16_string) != 8:
        raise ValueError("Input string is not a valid base16 string")

    # In decoding we have to combine two characters in the input string to a single number
    def base16_to_num(char: str) -> int:
        num: int = ord(char)
        if num >= ord('0') and num <= ord('9'):  # Char is a number
            return num - ord('0')
        elif num >= ord('a') and num <= ord('f'):
            return 10 + (num - ord('a'))
        else:
            raise ValueError("Input string contains a invalid base16 character")

    for i in range(8):
        chunk_num = base16_to_num(base16_string[i])
        output = output << 4 | chunk_num
    return output


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


def geometric_progression(g: int, sequence: str) -> int:
    """Returns the numeric value of the sequence with the given base g. Only works for 1 <= g < 36"""
    if g == 0:
        return 1
    k = len(sequence)
    result: int = 0
    for i, c in enumerate(sequence, 1):
        a = int(c, g)
        if a > g or a >= 26:
            raise ValueError
        result += a * pow(g, k - i)
    return result


def geometric_progression_rev(g: int, number: int) -> str:
    """Returns string representation of the number in the given base. Only works for 1 <= g < 36"""
    if g == 0:
        raise ValueError

    if number == 0:
        return "0"

    result: str = ""

    if g == 1:
        for i in range(number):
            result += "1"
        return result

    digits = "0123456789abcdefghijklmnopqrstuvwxyz"

    while number > 0:
        q, r = toymath.modulo(number, g)
        result += digits[r]
        number //= g
    return ''.join(reversed(result))


def binary2decimal(binary: str) -> int:
    return geometric_progression(2, binary)


def decimal2binary(decimal: int) -> str:
    return geometric_progression_rev(2, decimal)


def hex2decimal(hexa: str) -> int:
    return geometric_progression(16, hexa)


def decimal2hex(decimal: int) -> str:
    return geometric_progression_rev(16, decimal)
