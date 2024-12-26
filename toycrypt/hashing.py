# Hashing

# A hash function is any function that can be used to map data of arbitrary size to fixed-size values.
# The values returned by a hash function are called hash values, hash codes, hash digests, digests, or simply hashes.
# (Wikipedia)
# It can also be thought of mapping the given input to a different (often smaller) dimensions.
# This is often necessary in order to more easily handle something (e.g. compare hashes instead of whole files)

from toycrypt.util import *


class Hash:
    _number: int  # The hash number
    _string: str  # The hash encoded in hexadecimal using big-endian byte order

    def __init__(self, number: int):
        self.number = number
        self.string = encode16(number)

    def __str__(self):
        return f"Hash:{self.string}"

    def __eq__(self, other):
        if not isinstance(other, Hash):
            return False
        return self.number == other.number

    def get_string(self) -> str:
        return self.string

    def get_hash(self) -> int:
        return self.number


def hash_naive(input_str: str) -> hash:
    """
    Hashes the input string by simply adding the number values of each character
    :param input_str: any string
    :return: a hash object
    """
    hash_num = 0
    for character in input_str:
        hash_num += ord(character)  # Transform the character to its ASCII number
        hash_num = hash_num & 0xFFFFFFFF  # Make sure it stays a 32-bit unsigned number
    return Hash(hash_num)


def hash_allbits16(input_str: str) -> Hash:
    """
    Hashes the input
    :param input_str: any string
    :return: a hash object
    """
    seed: int = 123456789  # Seed the generator, such that many bits are flipped
    hash_num: int = seed
    for char in input_str:
        char_num = ord(char) * seed  # Make the number large so many bits are flipped
        hash_num = xor(char_num, hash_num)  # XOR the character and the current hash to produce the new hash
        hash_num = hash_num & 0xFFFF  # Make sure it stays a 16-bit unsigned number
    return Hash(hash_num)


def hash_allbits32(input_str: str) -> Hash:
    """
    Takes any string and outputs a hash object
    :param input_str: any string
    :return: a hash object
    """
    seed: int = 123456789  # Seed the generator, such that many bits are flipped
    hash_num: int = seed
    for char in input_str:
        char_num = ord(char) * seed  # Make the number large so many bits are flipped
        hash_num = xor(char_num, hash_num)  # XOR the character and the current hash to produce the new hash
        hash_num = hash_num & 0xFFFFFFFF  # Make sure it stays a 32-bit unsigned number
    return Hash(hash_num)

