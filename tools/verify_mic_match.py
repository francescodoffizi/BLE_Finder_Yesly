import sys
sys.path.append('tools')
from proto import parse_fields
from Cryptodome.Cipher import AES

# Target sniffed packet:
# F1 61 0E 00 03 A9 8C CF E3
cnt_bytes = bytes.fromhex("F1 61 0E 00")
cmd_byte = bytes.fromhex("03")
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

# Also scenarios in field 14
import base64
for item in plant.get(14, []):
    f = parse_fields(item)
    s_name = f.get(4, [b""])[0].decode(errors="ignore")
    k_b64 = f.get(5, [b""])[0].decode(errors="ignore")
    try:
        raw_key = base64.b64decode(k_b64)
        if len(raw_key) == 16:
            all_keys.append((f"Scenario: {s_name}", raw_key))
    except Exception:
        pass

print(f"Total keys loaded: {len(all_keys)}")

# HW addresses to test:
# Luce TV: 05:61:05:00:85:07 -> 05 61 05 00 85 07
# Gateway: 05:61:04:C0:66:36 -> 05 61 04 C0 66 36
# Or 05 61 00 00 85 07
# Or 05 61 85 07 00 00
# Or sender ESP: 05 61 ...
hw_list = [
    ("LuceTV_MAC", bytes.fromhex("05 61 05 00 85 07")),
    ("LuceTV_Short_8507", bytes.fromhex("05 61 85 07 00 00")),
    ("LuceTV_Short_05008507", bytes.fromhex("05 61 05 00 85 07")),
    ("LuceTV_Inv", bytes.fromhex("07 85 00 05 61 05")),
    ("GW_MAC", bytes.fromhex("05 61 04 C0 66 36")),
    ("GW_Short_6636", bytes.fromhex("05 61 66 36 00 00")),
    ("GW_Inv", bytes.fromhex("36 66 C0 04 61 05")),
    ("Zero_HW", bytes.fromhex("05 61 00 00 00 00")),
]

# AAD format from CreateInputBufferForAdv:
# [0x0C, 0xFF, 0x61, 0x05] + cnt_bytes + cmd_byte
aad_candidates = [
    ("Standard_AAD", bytes([0x0C, 0xFF, 0x61, 0x05]) + cnt_bytes + cmd_byte),
    ("Short_AAD_No_Len", bytes([0xFF, 0x61, 0x05]) + cnt_bytes + cmd_byte),
    ("Company_AAD", bytes([0x61, 0x05]) + cnt_bytes + cmd_byte),
    ("Data_Only_AAD", cnt_bytes + cmd_byte),
]

match_found = False
for k_desc, key in all_keys:
    for hw_desc, hw in hw_list:
        # Nonce is 13 bytes:
        # hw (6 bytes) + counter (4 bytes) + padding (3 bytes)
        nonce1 = hw + cnt_bytes + b"\x00\x00\x00"
        nonce2 = hw + cnt_bytes[::-1] + b"\x00\x00\x00"
        nonce3 = cnt_bytes + hw + b"\x00\x00\x00"
        
        for n_desc, nonce in [("hw+cnt+0", nonce1), ("hw+cnt_rev+0", nonce2), ("cnt+hw+0", nonce3)]:
            for aad_desc, aad in aad_candidates:
                try:
                    cipher = AES.new(key, AES.MODE_CCM, nonce=nonce, mac_len=4)
                    cipher.update(aad)
                    tag = cipher.digest()
                    if tag == target_mic:
                        print(f"!!! MATCH FOUND !!!")
                        print(f"Key: {k_desc} ({key.hex()})")
                        print(f"HW: {hw_desc} ({hw.hex()})")
                        print(f"Nonce mode: {n_desc} ({nonce.hex()})")
                        print(f"AAD mode: {aad_desc} ({aad.hex()})")
                        print(f"Tag: {tag.hex()}")
                        match_found = True
                        break
                except Exception:
                    pass

if not match_found:
    print("Direct exact match not found in initial grid, checking key counter variations...")
