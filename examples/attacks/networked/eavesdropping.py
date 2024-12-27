# Eavesdropping

# Eavesdropping is the act of secretly or stealthily listening to the private conversation or communications of others.
# Often without their consent in order to gather information.
# (Wikipedia)

#


from toycrypt.simulation import *

alice = Device("Alice")
bob = Device("Bob")
internet = Connection()  # Note: the internet is always a public connection as you cant rely on anything

# Both connect to the internet
alice.connect(internet)
bob.connect(internet)

# Now a third actor (an eavesdropper) connects as well
oscar = Device("Oscar")
internet.add_listener(oscar)

# Now when alice and bob talk, oscar can see the messages as well
alice.send(bob, "Hello Bob")
bob.send(alice, "Hello Alice")

for message in oscar.get_received_messages():
    print(message)
