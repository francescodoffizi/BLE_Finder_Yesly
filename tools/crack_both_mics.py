from Cryptodome.Cipher import AES
import struct

# Pair 1: Luce TV
mac1 = bytes.fromhex("05 61 05 00 85 07")
key1_master = bytes.fromhex("00112233445566778899aabbccddeeff")
cnt1 = bytes.fromhex("F1 61 0E 00")
cmd1 = bytes.fromhex("03")
target_mic1 = bytes.fromhex("A9 8C CF E3")

# Pair 2: Luce Balcone
mac2 = bytes.fromhex("05 61 01 00 56 0A")
key2_master = bytes.fromhex("00112233445566778899aabbccddeeff")
cnt2 = bytes.fromhex("F7 61 0E 00")
cmd2 = bytes.fromhex("03")
target_mic2 = bytes.fromhex("BA 99 45 EE")

# Common: Gateway
gw_mac = bytes.fromhex("05 61 04 C0 66 36")
gw_key = bytes.fromhex("00112233445566778899aabbccddeeff")

print("Testing permutations...")
