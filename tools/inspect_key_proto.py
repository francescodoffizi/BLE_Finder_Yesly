import sys
sys.path.append('tools')
from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])

for item in plant.get(11, []):
    f = parse_fields(item)
    k_type = f.get(2, [b""])[0].decode(errors="ignore")
    raw_key = f.get(7, [b""])[0].hex()
    f3 = f.get(3, [b""])[0]
    target_info = ""
    if f3:
        try:
            target_info = parse_fields(f3).get(1, [b""])[0].decode(errors="ignore")
        except Exception:
            target_info = f3.hex()
    # Check counter field 8
    cnt_field = f.get(8, [None])[0]
    cnt_val = ""
    if cnt_field:
        try:
            cf = parse_fields(cnt_field)
            cnt_val = f"subfields: {cf}"
        except Exception:
            cnt_val = cnt_field.hex()
    if "9f0e" in raw_key or "a34a" in raw_key or "6a04" in raw_key:
        print(f"Type: {k_type}, Target: {target_info}, Key: {raw_key}")
        print(f"  Field 8 (counter): {cnt_val}")
        for k in sorted(f.keys()):
            if k not in [2, 3, 7, 8]:
                print(f"  Field {k}: {f[k]}")
