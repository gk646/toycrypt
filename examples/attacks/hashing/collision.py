#  SPDX-License-Identifier: GPL-3.0-only

# Collision Attack

# Topics: Hashing, Digital Signatures

# A collision attack tries to find two different input values, that after hashing produce the same output
# When downloading files they are their hashes are often checked against precomputed ones.
# Finding such a collision allows attackers to substitute the file with on of their own, while the hash stays the same
# This is a lot easier than for example preimage or brute-force attacks as any collision is acceptable.
# This is formally called: https://en.wikipedia.org/wiki/Birthday_problem

# Known:
#   - The hash function used
# Hidden: -
# Wanted:
#   - Any two different input strings that hash to the same value

from toycrypt.hashing import *


# Start a collision attack with the given hash function and a input length (the length of our malicious payload)
def collision_attack(hash_function, input_length: int, max_tries: int = 10_000_000):
    print("-- Collision Attack --")
    print(f"    Using hash     : {hash_function.__name__}")

    hashes_set: dict[Hash, str] = {}  # Create a map of known hashes and the strings that produced them

    # For simplicity, we just try all numbers
    iterations: int = 0
    start_num: int = pow(10, input_length - 1)
    for start_num in range(start_num, start_num + max_tries):
        input_string = str(start_num)
        input_hash = hash_function(input_string)
        if input_hash in hashes_set:
            print(f"    Found collision after {iterations} attempts!")
            print(f"    Inputs {input_string} and {hashes_set[input_hash]} both map to:{input_hash.get_string()}")
            return
        hashes_set[input_hash] = input_string  # Insert the mapping
        iterations += 1


# Exposes the weakness of using addition in the hash function
# This happens regardless of length and is thus very dangerous (usually length increases computation time needed)
measure(collision_attack, hash_function=hash_addition, input_length=4)
measure(collision_attack, hash_function=hash_allbits16, input_length=4)
measure(collision_attack, hash_function=hash_allbits32, input_length=4)

# This is the only function who does not suffer from the glaring addition weakness - but another collision is found rather quickly
measure(collision_attack, hash_function=hash_toycrypt, input_length=4)
