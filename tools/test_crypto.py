from cryptography.hazmat.primitives import cmac, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import struct

k_gateway = bytes.fromhex("00112233445566778899aabbccddeeff")
k_lucetv = bytes.fromhex("00112233445566778899aabbccddeeff")
k_scenario = bytes.fromhex("00112233445566778899aabbccddeeff")

target_mic1 = bytes.fromhex("f7219653")
target_mic2 = bytes.fromhex("93b22edd")

# Payload prefix: C9 61 0E 00 03
p1 = bytes.fromhex("c9610e0003")
# With company ID: 61 05 or 05 61
# Let's test combinations
candidates_keys = [("gateway", k_gateway), ("lucetv", k_lucetv), ("scenario", k_scenario)]

print("Testing CMAC matches...")
for name, k in candidates_keys:
    # Test raw p1
    for prefix in [b"", b"\x61\x05", b"\x05\x61"]:
        data = prefix + p1
        c = cmac.CMAC(algorithms.AES(k))
        c.update(data)
        tag = c.finalize()
        if tag[:4] == target_mic1 or tag[:4] == target_mic1[::-1]:
            print(f"MATCH CMAC! Key: {name}, prefix: {prefix.hex()}, tag: {tag[:4].hex()}")

print("Crypto test done.")
