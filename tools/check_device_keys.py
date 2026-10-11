import json
from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])

lucetv_uuid = "bfcd8bfd-d698-457a-9345-4cb38028a98f"

for item in plant.get(11, []):
    f = parse_fields(item)
    k_type = f.get(2, [b""])[0].decode(errors="ignore")
    f3 = f.get(3, [b""])
    target_uuid = ""
    if f3 and isinstance(f3[0], bytes):
        target_uuid = parse_fields(f3[0]).get(1, [b""])[0].decode(errors="ignore")
    if target_uuid == lucetv_uuid:
        raw_key = f.get(7, [b""])[0]
        print(f"Key for Luce TV: type={k_type} key={raw_key.hex()}")
