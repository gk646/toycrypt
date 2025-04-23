#  SPDX-License-Identifier: GPL-3.0-only

from toycrypt import toymath
from util import xor, decimal2hex, hex2decimal


class Key:
    _number: int

    def __init__(self, number: int):
        self._number = number

    def __str__(self):
        return decimal2hex(self._number)


class KeyPair:
    _public: Key
    _private: Key

    def __init__(self, private: Key, public: Key):
        self._private = private
        self._public = public

    def __str__(self):
        return f"Private:{self._private} / Public:{self._public}"


def encrypt_xor(input_string: str, secret_key: int, key_bytes: int = 4) -> str:
    """
    Encrypts the given string using the xor cipher with the key repeating each key_bytes many bytes
    Changing the byte length of the key allows to test the impact its impact on the cipher strength
    :param input_string: the string to encode
    :param secret_key: the secret key
    :param key_bytes: after how many bytes the key is repeated
    :return: the encrypted string
    """
    output = ""
    key_index = 0
    for byte in input_string:
        input_byte: int = ord(byte)
        key_byte = (secret_key >> 8 * key_index) & 0xFF  # Extract the first byte
        cypher_byte = xor(input_byte, key_byte)
        output += chr(cypher_byte)
        key_index = (key_index + 1) % key_bytes  # Repeat the key
    return output


def decrypt_xor(cipher_text: str, secret_key: int, key_length: int = 4) -> str:
    """
    Decrypts the given cipher text using the xor cipher. Key and length must be the same as used for encryption
    :param cipher_text: the encrypted string
    :param secret_key: same key used for encryption
    :param key_length: same length used for encryption
    :return: the decrypted string
    """
    # xor encryption has a few special properties
    #       - symmetrical: applying
    return encrypt_xor(cipher_text, secret_key, key_length)


def diffie_hellman_private(p: int, g: int, secret: int) -> Key:
    q, r = toymath.modulo(pow(g, secret), p)
    # Note: this is NOT a key in the sens of public key cryptography
    return Key(r)


def diffie_hellman_exchange(p: int, g: int, secret: int, other: Key) -> Key:
    shared_secret = pow(other._number, secret, p)
    return Key(shared_secret)
