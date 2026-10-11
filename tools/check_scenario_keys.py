import base64
from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])
for item in plant.get(14, []):
    f = parse_fields(item)
    name = f.get(4, [b""])[0].decode(errors="ignore")
    k_b64 = f.get(5, [b""])[0].decode(errors="ignore")
    raw_key = base64.b64decode(k_b64)
    print(f"Scenario: {name:<25} Key (hex): {raw_key.hex()} (len: {len(raw_key)})")
