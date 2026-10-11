from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])
gw_uuid = b"52292c50-5f6f-400e-84a1-a7d51e680dd0"

for k, vals in plant.items():
    for idx, v in enumerate(vals):
        if isinstance(v, bytes) and gw_uuid in v:
            print(f"Found in Field {k} item {idx}!")
            try:
                sub = parse_fields(v)
                for sk, sv in sub.items():
                    print(f"   sub {sk}: {sv}")
            except Exception:
                print(f"   raw: {v}")
