# Brute Force Attack
# Topics: Hashing, Passwords

# A brute force attack focuses on finding an input that produces a specific hash value (a so-called preimage)
# This is helpful as usually for password authentication you store only the hash of the password (not in plain text)
# If you can now find any input that computes to the same hash you can authenticate yourself without knowing the real password
# Note: A brute-force attack is similar to a pre-image attacks, but you do not try to exploit any weakness.
#       It relies solely on trying all possible inputs (exhaustive search).
#       The found pre-image might be the original password (but the attacker doesnt know that)

# Known:
#   - The password hash (e.g. stolen from a database)
#   - The hash function used
# Hidden:
#   - The original password string
# Wanted:
#   - Any input string that hashes to the same value as the original password

from toycrypt.hashing import *
from itertools import product


# In order to attack now we have to try all possible combination of characters until anyone matches the known password hash
def brute_force(hash_function, password: str, max_iterations: int = 10_000_000):
    print("-- Brute Force Attack --")
    print(f"    Using hash     : {hash_function.__name__}")
    print(f"    Using Password : {password}")
    password_hash = hash_function(password)  # Hash the password
    print(f"    Hashed password: {password_hash.get_string()}")

    # Simulates the authentication process - you can only check a plaintext string against the known password
    # This is because every input will be hashed before checking - so you need something that hashes to the known hash
    def authenticate(input_password: str) -> bool:
        input_password_hash = hash_function(input_password)
        return password_hash == input_password_hash

    # Consider only the visible ASCII characters https://www.ascii-code.com/
    # Try any combination of allowed characters - lowercase letters and digits
    chars = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]

    print("\n\tStarting attempts...")
    iterations = 0
    for length in range(1, 10 + 1):  # Try up to a length of 10
        # Try all possible combinations - like you would try on a 4 digit bike lock
        # 0000 -> 0001 ... -> 0009 -> 0010 -> 0011 ... -> 0100 -> 0101 ...
        for current_string_tuple in product(chars, repeat=length):
            # Build the current string from counters
            current_string = ''.join(current_string_tuple)

            if authenticate(current_string):
                # We have found an input that computes to the same hash
                # For the authentication process it now has the same power as the original password!
                if current_string == password:
                    print(f"    Found original password after {iterations} attempts!")
                else:
                    print(f"    Found pre-image after {iterations} attempts!")
                print(f"    Value (Pre-image): {current_string}")
                return

            iterations += 1
            if iterations % 1_000_000 == 0:
                print(f"    Completed {iterations} tries!")
            if iterations == max_iterations:
                print(f"    Could not find a preimage after {iterations} tries!")
                return


# Measure the time it takes for different hash functions to find the

# Note how the input length increases the time taken - but both are cracked quite fast as the hash function has weaknesses
measure(brute_force, password="1234578", hash_function=hash_addition)
measure(brute_force, password="123456789", hash_function=hash_addition)

# Using a better hash function drastically increases time taken, even on smaller inputs

# Using only a 16 bit range makes it much more likely to find a preimage (as there are fewer values in the output space)
measure(brute_force, password="12345", hash_function=hash_allbits16)
measure(brute_force, password="123456", hash_function=hash_allbits16)

# Instead of finding another preimage we find the original password here (as we simply iterate all possibilities and arrive at the password)
# This means the hash function has some level of robustness
measure(brute_force, password="1234", hash_function=hash_allbits32)
measure(brute_force, password="1234", hash_function=hash_toycrypt)

# The only two uncracked hash function (can take up to 30 seconds)
measure(brute_force, password="12345", hash_function=hash_allbits32)
measure(brute_force, password="12345", hash_function=hash_toycrypt)
