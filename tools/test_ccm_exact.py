from Cryptodome.Cipher import AES
import struct

# Captured packet:
# Packet: F1 61 0E 00 03 A9 8C CF E3
# Target: Luce TV (05:61:05:00:85:07)
# Counter in packet: F1 61 0E 00 -> 0x000E61F1 (942577) or little-endian bytes: F1 61 0E 00

# Let's check IV (13 bytes):
# IV bytes 0..5 = hwaddr
# IV bytes 6..9 = counter bytes
# IV bytes 10..12 = 0x00, 0x00, 0x00

# Candidates for hwaddr (6 bytes):
# 1. Device MAC: 05 61 05 00 85 07
# 2. Gateway BLE addr: 05 61 04 C0 66 36
# 3. Gateway short addr: 05 61 66 36 00 00
# 4. Inverted MAC: 07 85 00 05 61 05

# Candidates for Key:
# 1. Luce TV Master Key: 00112233445566778899aabbccddeeff
# 2. Gateway Key: 00112233445566778899aabbccddeeff
# 3. Scenario Keys: 00112233445566778899aabbccddeeff, 00112233445566778899aabbccddeeff

keys = {
    "LuceTV_Master": bytes.fromhex("00112233445566778899aabbccddeeff"),
    "Gateway_Key": bytes.fromhex("00112233445566778899aabbccddeeff"),
    "Scenario_1": bytes.fromhex("00112233445566778899aabbccddeeff"),
    "Scenario_2": bytes.fromhex("00112233445566778899aabbccddeeff"),
}

counter_bytes = bytes.fromhex("F1 61 0E 00")
cmd_byte = bytes.fromhex("03")
expected_mic = bytes.fromhex("A9 8C CF E3")

# Let's check hwaddr candidates:
hw_candidates = [
    ("Dev_MAC_BE", bytes.fromhex("05 61 05 00 85 07")),
    ("Dev_MAC_LE", bytes.fromhex("07 85 00 05 61 05")),
    ("Dev_Short_1", bytes.fromhex("05 61 85 07 00 00")),
    ("Dev_Short_2", bytes.fromhex("05 61 00 00 85 07")),
    ("Dev_ID_4bytes", bytes.fromhex("05 61 05 00 85 07")[:6]),
    ("GW_MAC_BE", bytes.fromhex("05 61 04 C0 66 36")),
    ("GW_MAC_LE", bytes.fromhex("36 66 C0 04 61 05")),
]

# inputBuffer (AAD):
# Byte 0: 0x0C
# Byte 1: 0xFF
# Byte 2: 0x61
# Byte 3: 0x05
# Byte 4..7: counter_bytes
# Byte 8: cmd_byte (0x03)
aad = bytes([0x0C, 0xFF, 0x61, 0x05]) + counter_bytes + cmd_byte
print("AAD:", aad.hex())

found = False
for k_name, key in keys.items():
    for hw_name, hw in hw_candidates:
        # Build 13-byte IV
        # IV = hw (6 bytes) + counter_bytes (4 bytes) + 3 zero bytes
        iv1 = hw + counter_bytes + b"\x00\x00\x00"
        iv2 = hw + counter_bytes[::-1] + b"\x00\x00\x00"
        iv3 = counter_bytes + hw + b"\x00\x00\x00"
        for iv_name, iv in [("hw+cnt+0", iv1), ("hw+cnt_rev+0", iv2), ("cnt+hw+0", iv3)]:
            if len(iv) != 13: continue
            try:
                cipher = AES.new(key, AES.MODE_CCM, nonce=iv, mac_len=4)
                cipher.update(aad)
                tag = cipher.digest()
                if tag == expected_mic:
                    print(f"MATCH FOUND! Key: {k_name}, HW: {hw_name}, IV: {iv_name}")
                    print(f"Tag: {tag.hex()} == {expected_mic.hex()}")
                    found = True
            except Exception as e:
                pass

if not found:
    print("Testing broader variations...")
