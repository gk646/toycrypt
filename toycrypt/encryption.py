#  SPDX-License-Identifier: GPL-3.0-only

# Encryption

from util import xor


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
