import struct

# Data gathered:
# Luce TV (85 07):
# Turn OFF:
# Seq 0xEF, Cmd 0x03 -> MIC 1C 9E CD 44
# Seq 0xF0, Cmd 0x02 -> MIC C6 15 26 56
# Turn ON:
# Seq 0xF1, Cmd 0x03 -> MIC A9 8C CF E3
# Seq 0xF2, Cmd 0x02 -> MIC A1 F2 4A 91
# Turn OFF:
# Seq 0xF3, Cmd 0x03 -> MIC A4 13 DC 50
# Seq 0xF4, Cmd 0x02 -> MIC 05 5C 0A F7

# Luce Balcone Soggiorno (56 0A):
# Turn ON:
# Seq 0xF7, Cmd 0x03 -> MIC BA 99 45 EE
# Seq 0xF8, Cmd 0x02 -> MIC FB 5E C5 2E
# Turn OFF:
# Seq 0xF9, Cmd 0x03 -> MIC 3D 38 D8 8E
# Seq 0xFA, Cmd 0x02 -> MIC 41 83 1C 69

print("Command Seq & MIC table:")
data = [
    ("Luce TV OFF", 0xEF, 3, "1c9ecd44"),
    ("Luce TV OFF", 0xF0, 2, "c6152656"),
    ("Luce TV ON",  0xF1, 3, "a98ccfe3"),
    ("Luce TV ON",  0xF2, 2, "a1f24a91"),
    ("Luce TV OFF", 0xF3, 3, "a413dc50"),
    ("Luce TV OFF", 0xF4, 2, "055c0af7"),
    ("Balcone ON",  0xF7, 3, "ba9945ee"),
    ("Balcone ON",  0xF8, 2, "fb5ec52e"),
    ("Balcone OFF", 0xF9, 3, "3d38d88e"),
    ("Balcone OFF", 0xFA, 2, "41831c69"),
]

for name, seq, cmd, mic_hex in data:
    mic_int = int.from_bytes(bytes.fromhex(mic_hex), "big")
    mic_le = int.from_bytes(bytes.fromhex(mic_hex), "little")
    print(f"{name:<15} Seq: 0x{seq:02X} ({seq:3d}) Cmd: {cmd} | MIC BE: 0x{mic_int:08X} LE: 0x{mic_le:08X}")
