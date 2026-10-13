import json
from pathlib import Path
from cryptography.hazmat.primitives import cmac, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import struct

# Load keys
keys_file = Path(__file__).parent.parent / "keys.json"
with open(keys_file) as f:
    plant_data = json.load(f)

lucetv_master = bytes.fromhex("00112233445566778899aabbccddeeff")
gateway_key = bytes.fromhex("00112233445566778899aabbccddeeff")
scenario_spegni = bytes.fromhex("00112233445566778899aabbccddeeff")
scenario_chiudi = bytes.fromhex("00112233445566778899aabbccddeeff")

test_keys = [
    ("LuceTV_Master", lucetv_master),
    ("Gateway_Key", gateway_key),
    ("Scenario_Spegni", scenario_spegni),
    ("Scenario_Chiudi", scenario_chiudi),
]

# We test pair:
# p = EF 61 0E 00 03 (Turn OFF)
# mic = 1C 9E CD 44
# Associated actuator telemetry counter: C4 F9 (or C4 FA)
# Target address: 85 07

target_mic = bytes.fromhex("1c9ecd44")
p = bytes.fromhex("ef610e0003")

# In Bluetooth Mesh or proprietary mesh, a network MIC / transport MIC is computed as:
# AES-CMAC(Key, Nonce || Data) or AES-CCM
# Let's test standard AES-CMAC over various inputs:
for kname, key in test_keys:
    # Try different IVs / Nonces
    candidates = [
        p,
        p + bytes.fromhex("8507"),
        bytes.fromhex("8507") + p,
        bytes.fromhex("056105008507") + p,
        p + bytes.fromhex("c4f9"),
        p + bytes.fromhex("f9c4"),
        bytes.fromhex("8507") + bytes.fromhex("c4f9") + p,
        bytes.fromhex("056104c06636") + p, # Gateway MAC + p
        p + bytes.fromhex("056104c06636"),
        # With Bluetooth Company ID
        b"\x61\x05" + p,
        b"\x05\x61" + p,
    ]
    for c_data in candidates:
        # CMAC
        c = cmac.CMAC(algorithms.AES(key))
        c.update(c_data)
        tag = c.finalize()
        if tag[:4] == target_mic or tag[:4] == target_mic[::-1]:
            print(f"[FOUND CMAC!] Key: {kname}, Data: {c_data.hex()}, Tag: {tag[:4].hex()}")

print("Candidate scan finished.")
