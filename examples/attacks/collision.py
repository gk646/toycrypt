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
def collision_attack(hash_function, input_length : int):
    hashes_set = set() # Create a set out of the computed hashes (the hashes we know)





