#  SPDX-License-Identifier: GPL-3.0-only

# Eavesdropping

# Eavesdropping is the act of secretly or stealthily listening to the private conversation or communications of others.
# Often without their consent in order to gather information.
# (Wikipedia)

#


from toycrypt.simulation import *

# Note: the internet is always a public connection as you cant rely on anything
internet = Connection()

# Any communication can have a third pary (an eavesdropper) connected as well
eve = Device("Eve")
internet.add_listener(eve)

# Alice and Bob now want to send messages to each other
alice = Device("Alice")
bob = Device("Bob")
internet = Connection()  # Note: the internet is always a public connection as you cant rely on anything

# Both connect to the internet
alice.connect(internet)
bob.connect(internet)

# Now when alice and bob talk, eve can see the messages as well
alice.send(bob, "Hello Bob")
bob.send(alice, "Hello Alice")

for message in eve.get_received_messages():
    print(message)

# Now Alice and Bob decide to encrypt their traffic
# But first they have to


# To combat sharing the key over the public channel you can use Diffie-Hellman key exchange.
# https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
# It works by