from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])
gw = parse_fields(plant[17][0])
for k, v in gw.items():
    print(k, v)
