#  SPDX-License-Identifier: GPL-3.0-only

# Hashing

# A hash function is any function that can be used to map data of arbitrary size to fixed-size values.
# The values returned by a hash function are called hash values, hash codes, hash digests, digests, or simply hashes.
# (Wikipedia)
# It can also be thought of mapping the given input to a different (often smaller) dimensions.
# This is often necessary in order to more easily handle something (e.g. compare hashes instead of whole files)
# Hash functions have different purposes and properties and are built with different techniques
# Showcased here are simple all-purpose hash functions that use:
#       - naive addition
#       - naive addition but multiplied with a big number (to use the whole number space)
#       - limiting the output space (16-bit and 32-bit)
#       - using an evolving state to achieve avalanche effect

from toycrypt.util import *


class Hash:
    """
    A hash object that contains the numerical and string representation
    """
    _number: int  # The hash number
    _string: str  # The hash encoded in hexadecimal using big-endian byte order

    def __init__(self, number: int):
        self.number = number
        self.string = decimal2hex(number)

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

    def __hash__(self):
        return self.number


class HashPair:
    """
    A pair of a hash object and the input that produced it
    """
    _hash: Hash  # The hash
    _input: str  # Input that produced this hash

    def __init__(self, input_val: str, hash_val: Hash):
        self._hash = hash_val
        self._input = input_val

    def get_hash(self) -> Hash:
        return self._hash

    def get_input(self) -> str:
        return self._input


def hash_addition(input_str: str) -> Hash:
    """
    Hashes the input string by simply adding the number values of each character
    This function has a major weakness, because the order of addition is not relevant
    This can easily be exploited: "15" hashes to same value as "51"
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
    Hashes the input using big numbers to change all bit on every input and using the XOR operation
    Limits itself to only using the 16-bit (unsigned) space: 0 - 65,536
    :param input_str: any string
    :return: a hash object
    """
    seed: int = 123456789  # Seed the generator to flip most bits
    hash_num: int = seed
    for char in input_str:
        char_num = ord(char) * seed  # Make the number large so many bits are flipped
        hash_num = xor(char_num, hash_num)  # XOR the character and the current hash to produce the new hash
        hash_num = hash_num & 0xFFFF  # Make sure it stays a 16-bit unsigned number
    return Hash(hash_num)


def hash_allbits32(input_str: str) -> Hash:
    """
    Hashes the input using big numbers to change all bit on every input and using the XOR operation
    Limits itself to only using the 32-bit (unsigned) space: 0 - 4,294,967,295
    :param input_str: any string
    :return: a hash object
    """
    seed: int = 123456789  # Seed the generator to flip most bits
    hash_num: int = seed
    for char in input_str:
        char_num = ord(char) * seed  # Make the number large so many bits are flipped
        hash_num = xor(char_num, hash_num)  # XOR the character and the current hash to produce the new hash
        hash_num = hash_num & 0xFFFFFFFF  # Make sure it stays a 32-bit unsigned number
    return Hash(hash_num)


def hash_toycrypt(input_str: str) -> Hash:
    """
    Hashes the input using big numbers to change all bits on every input using an XOR operation
    Additionally it uses an evolving state to achieve an avalanche effect (each input affects all following ones)
    Limits itself to only using the 32-bit (unsigned) space: 0 - 4,294,967,295
    :param input_str:
    :return: a hash object
    """
    seed: int = 123456789  # Seed the generator to flip most bits
    state = seed  # Keep a state that changes with every input
    hash_num: int = state
    for char in input_str:
        char_num = ord(char) * state  # Make the number large so many bits are flipped
        hash_num = xor(char_num, hash_num)  # XOR the character and the current hash to produce the new hash
        state = xor(hash_num, state)  # XOR the state with the current hash
        hash_num = hash_num & 0xFFFFFFFF  # Make sure it stays a 32-bit unsigned number
    return Hash(hash_num)
