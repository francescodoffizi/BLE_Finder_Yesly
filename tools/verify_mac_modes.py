import sys
sys.path.append('tools')
from proto import parse_fields
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Hash import CMAC

target_mic = bytes.fromhex("A9 8C CF E3")

# Load all keys from plant_dump.bin
with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])

all_keys = []
for item in plant.get(11, []):
    f = parse_fields(item)
    k_type = f.get(2, [b""])[0].decode(errors="ignore")
    raw_key = f.get(7, [b""])[0]
    if len(raw_key) == 16:
        all_keys.append((k_type, raw_key))

for item in plant.get(14, []):
    f = parse_fields(item)
    s_name = f.get(4, [b""])[0].decode(errors="ignore")
    k_b64 = f.get(5, [b""])[0].decode(errors="ignore")
    try:
        raw_key = base64.b64decode(k_b64)
        if len(raw_key) == 16:
            all_keys.append((f"Scenario:{s_name}", raw_key))
    except Exception:
        pass

# Candidate data inputs to MAC
inputs = [
    # Full AAD
    bytes.fromhex("0C FF 61 05 F1 61 0E 00 03"),
    # Without length
    bytes.fromhex("FF 61 05 F1 61 0E 00 03"),
    # Company + payload
    bytes.fromhex("61 05 F1 61 0E 00 03"),
    # Just packet payload
    bytes.fromhex("F1 61 0E 00 03"),
    # With actuator MAC
    bytes.fromhex("05 61 05 00 85 07 F1 61 0E 00 03"),
    bytes.fromhex("05 00 85 07 F1 61 0E 00 03"),
    bytes.fromhex("85 07 F1 61 0E 00 03"),
    # With gateway MAC
    bytes.fromhex("05 61 04 C0 66 36 F1 61 0E 00 03"),
    bytes.fromhex("66 36 F1 61 0E 00 03"),
]

print(f"Testing {len(all_keys)} keys across {len(inputs)} input formats...")

# 1. Test AES-CMAC
for k_desc, key in all_keys:
    for inp in inputs:
        c = CMAC.new(key, ciphermod=AES)
        c.update(inp)
        tag = c.digest()
        if tag[:4] == target_mic or tag[:4] == target_mic[::-1] or tag[-4:] == target_mic or tag[-4:] == target_mic[::-1]:
            print(f"[FOUND CMAC!] Key: {k_desc} Input: {inp.hex()} Tag: {tag.hex()}")

# 2. Test AES-CBC-MAC
for k_desc, key in all_keys:
    for inp in inputs:
        # pad to 16 bytes
        pad_len = 16 - (len(inp) % 16)
        if pad_len == 16: padded = inp
        else: padded = inp + b"\x00" * pad_len
        
        cipher = AES.new(key, AES.MODE_CBC, iv=b"\x00" * 16)
        ct = cipher.encrypt(padded)
        tag = ct[-16:]
        if tag[:4] == target_mic or tag[:4] == target_mic[::-1] or tag[-4:] == target_mic or tag[-4:] == target_mic[::-1]:
            print(f"[FOUND CBC-MAC (zero IV)!] Key: {k_desc} Input: {inp.hex()} Tag: {tag.hex()}")

print("Search completed.")
