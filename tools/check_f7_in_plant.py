from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

# Let's search if BA 99 45 EE or 3D 38 D8 8E or 1C 9E CD 44 appear in plant dump!
mics = [
    bytes.fromhex("ba9945ee"),
    bytes.fromhex("fb5ec52e"),
    bytes.fromhex("3d38d88e"),
    bytes.fromhex("41831c69"),
    bytes.fromhex("1c9ecd44"),
    bytes.fromhex("a98ccfe3"),
]

for m in mics:
    pos = data.find(m)
    print(f"MIC {m.hex()}: in plant_dump? {pos != -1} (pos: {pos})")
    pos_rev = data.find(m[::-1])
    print(f"MIC {m[::-1].hex()}: in plant_dump? {pos_rev != -1} (pos: {pos_rev})")
