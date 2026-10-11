import json
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import struct

# Keys:
gateway_key = bytes.fromhex("00112233445566778899aabbccddeeff")
lucetv_master = bytes.fromhex("00112233445566778899aabbccddeeff")

# Captured packet:
# F1 61 0E 00 03 [A9 8C CF E3]
# Seq = 0xF1, Cmd = 0x03, MIC = A9 8C CF E3
# Target: 05:61:05:00:85:07
# Actuator telemetry counter: C5 0B / C5 0C

# In Bluetooth Mesh AES-CCM:
# Tag length is 4 bytes (tag_length=4) or 8 bytes
# Nonce is 13 bytes!
# Data payload is plaintext, authenticated with CCM.

for k_name, k in [("Gateway", gateway_key), ("LuceTV", lucetv_master)]:
    aesccm = AESCCM(k, tag_length=4)
    # Test possible 13-byte nonces:
    # E.g. [Nonce type (1B)] [Seq (3B)] [Src (2B)] [Dst (2B)] [IV Index (4B)] [Pad (1B)]
    # Or variations
    seq_bytes = bytes([0xF1, 0x00, 0x00])
    src_gw = bytes.fromhex("6636") # Gateway MAC short addr: 66 36 (from 05:61:04:C0:66:36)
    dst_act = bytes.fromhex("8507") # Actuator short addr: 85 07
    
    # Try typical nonces:
    nonces = [
        bytes.fromhex("00") + seq_bytes + src_gw + dst_act + b"\x00" * 5,
        bytes.fromhex("01") + seq_bytes + src_gw + dst_act + b"\x00" * 5,
        bytes.fromhex("02") + seq_bytes + src_gw + dst_act + b"\x00" * 5,
        b"\x00" * 12 + bytes([0xF1]),
        bytes([0xF1]) + b"\x00" * 12,
        bytes.fromhex("056104c06636") + bytes([0xF1]) + b"\x00" * 6,
    ]
    
    p = bytes.fromhex("610e0003")
    target_tag = bytes.fromhex("a98ccfe3")
    
    for n in nonces:
        if len(n) != 13:
            continue
        try:
            # Encrypt empty payload with associated data p
            ct = aesccm.encrypt(n, b"", p)
            if ct == target_tag or ct == target_tag[::-1]:
                print(f"[FOUND CCM!] Key: {k_name} Nonce: {n.hex()} Tag: {ct.hex()}")
        except Exception:
            pass

print("CCM test completed.")
