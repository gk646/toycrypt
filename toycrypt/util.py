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


def encode16_str(input_string: str) -> str:
    """
    Encodes the given input string to base16 (hexadecimal) representation
    :param input_string: a string of any length
    :return: the base16 representation of the input string
    """
    output = ""  # Start with the empty string

    # Each byte of the input is split into two 4 bit values (0-16)
    # Then transferred to its character representation

    def get_base_16char(number: int) -> str:
        if number < 10:  # 0 - 9 stays the same
            return str(number)
        return chr(ord('a') + (number - 10))

    for byte in input_string:
        byte_num = ord(byte)  # Convert byte to a number (32 bit)

        # Only look at the first 8 bits - split it into two 4 bit chunks
        # Extract the first 4 bits of the 8 bits (high nibble) - shift them to the left and zero everything else
        first_bits = (byte_num >> 4) & 0b00001111
        # Extract the last 4 bits - already in the correct position (low nibble) - zero everything else
        second_bits = byte_num & 0b00001111

        # Convert both 4-bit chunks to their hexadecimal representation
        output += get_base_16char(first_bits)
        output += get_base_16char(second_bits)
    return output


