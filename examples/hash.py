from toycrypt import util, hashing

print(util.encode16(1192210))
print(util.decode16("00123112"))
print(hashing.hash_naive("Password"))