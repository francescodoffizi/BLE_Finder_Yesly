from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])

gw_uuid = "52292c50-5f6f-400e-84a1-a7d51e680dd0"

for item in plant.get(12, []):
    f = parse_fields(item)
    uid = f.get(1, [b""])[0].decode(errors="ignore")
    if uid == gw_uuid:
        print("Found Gateway in Field 12!")
        for k, v in f.items():
            print(k, v)
