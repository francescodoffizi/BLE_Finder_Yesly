import json
from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])
print("Keys in plant message:", plant.keys())

for k, vals in plant.items():
    print(f"\n--- Field {k} (count: {len(vals)}) ---")
    for i, v in enumerate(vals[:3]):
        if isinstance(v, bytes):
            try:
                sub = parse_fields(v)
                print(f"  [{i}] (subfields: {list(sub.keys())})")
                for sk, sv in sub.items():
                    sample = sv[0] if sv else None
                    if isinstance(sample, bytes):
                        print(f"      subfield {sk}: {sample[:40].hex()} ({sample[:40]})")
                    else:
                        print(f"      subfield {sk}: {sample}")
            except Exception:
                print(f"  [{i}] bytes len={len(v)}: {v[:50].hex()}")
        else:
            print(f"  [{i}] varint: {v}")
