import json
from pathlib import Path
from cryptography.hazmat.primitives import cmac, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import struct

# Actuator Response:
# 45 00 85 07 A2 A2 00 00 C1 1B 11 [6F 9A 5E 76] FF FF FF FF FF
# Command Packet:
# DB 61 0E 00 03 [6F 9A 5E 76]

# Key candidates:
keys = {
    "LuceTV_Master": bytes.fromhex("00112233445566778899aabbccddeeff"),
    "Gateway_Key": bytes.fromhex("00112233445566778899aabbccddeeff"),
    "Scenario_ChiudiCasa": bytes.fromhex("00112233445566778899aabbccddeeff"),
    "Scenario_SpegniLuci": bytes.fromhex("00112233445566778899aabbccddeeff"),
}

# The 4 bytes MIC
target_mic = bytes.fromhex("6f9a5e76")

# Components that might be in the authenticated data:
# Command: seq=0xDB, cmd=0x61, 0E, 00, 03
# Actuator: MAC 05:61:05:00:85:07 (or 85 07), counter 0xC11B, state 00 00, ch A2 A2

# Let's test what AES block cipher encrypts into target_mic or if it's AES-ECB
for kname, k in keys.items():
    # 1. AES-ECB test: does AES_enc(data)[:4] == target_mic?
    cipher = Cipher(algorithms.AES(k), modes.ECB())
    enc = cipher.encryptor()
    
    # Try constructing 16-byte blocks with command seq (DB), target address (85 07), counter (C1 1B), etc.
    # Variations of 16-byte inputs:
    inputs = [
        # DB 61 0E 00 03 + 85 07 + ...
        bytes.fromhex("db610e0003") + bytes.fromhex("8507") + b"\x00" * 9,
        bytes.fromhex("db610e0003") + b"\x00" * 11,
        bytes.fromhex("056105008507") + bytes.fromhex("db610e0003") + b"\x00" * 5,
        bytes.fromhex("8507") + bytes.fromhex("db610e0003") + b"\x00" * 9,
        bytes.fromhex("c11b") + bytes.fromhex("8507") + bytes.fromhex("db610e0003") + b"\x00" * 7,
        # Counter based
        struct.pack("<H", 0xC11B) + bytes.fromhex("8507") + b"\x00" * 12,
        struct.pack(">H", 0xC11B) + bytes.fromhex("8507") + b"\x00" * 12,
    ]
    for inp in inputs:
        out = enc.update(inp)
        if out[:4] == target_mic or out[:4] == target_mic[::-1] or out[-4:] == target_mic or out[-4:] == target_mic[::-1]:
            print(f"[MATCH ECB!] {kname} inp={inp.hex()} out={out.hex()}")

print("ECB candidate scan finished.")
