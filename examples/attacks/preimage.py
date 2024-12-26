# Preimage Attack
# Hashing, Passwords

# A preimage attack focuses on finding an input that produces a specific hash value (e.g. a stored password hash)
# This is helpful as usually for password authentication you store only the hash of the password (not in plain text)
# If you can now find any input that computes to the same hash you can authenticate yourself without knowing the real password

# Known:
#   - The password hash (e.g. stolen from a database)
#   - The hashing algorithm used
# Hidden:
#   - The original password string

from toycrypt.hashing import *
import time

password = "mypassword123"
password_hash = hash_naive(password)

print("-- Pre Image Attack --")
print(f"Password       : {password}")
print(f"Hashed password: {password_hash.get_string()}")


# Simulates the authentication process - you can only check a plaintext string against the known password
# This is because every input will be hashed before checking - so you need something that hashes to the known hash
def authenticate(input_password: str, hash_function) -> bool:
    input_password_hash = hash_function(input_password)
    return password_hash == input_password_hash

# In order to attack now we have to try all possible combination of characters until anyone matches the known password hash
def preimage_attack( hash_function, ):
    # Consider only the visible ASCII characters https://www.ascii-code.com/
    # Try any combination of allowed characters - lowercase letters and digits
    chars = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
        "u", "v", "w", "x", "y", "z",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]
    length = 10
    counters = [0] * length  # Have a counter for each field that - like a numbers lock for a bike
    iterations = 0
    while True:
        # Build the current string from counters
        current_string = ''.join(chars[counters[i]] for i in range(length))

        if authenticate(current_string, hash_function):
            print(f"Successfully found a input that hashes to the same value: {current_string}")
            break

        # Try all possible combinations - like you would try on a 4 digit bike lock
        # 0000 -> 0001 ... -> 0009 -> 0010 -> 0011 ... -> 0100 -> 0101 ...
        for i in range(length - 1, -1, -1):
            counters[i] += 1
            if counters[i] < len(chars):
                break
            counters[i] = 0  # Reset current counter and carry to the next
        else:
            break  # Break if all counters are reset (end of loop)
        iterations += 1
        if iterations % 100_000 == 0:
            print(f"Completed {iterations} tries!")


start_time = time.time()  # Measure the attack time

preimage_attack(hash_naive)

end_time = time.time()  # Measure the attack time

print(f"Took: {end_time - start_time}s")
