import struct
from pathlib import Path

so_path = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so")
data = so_path.read_bytes()

idx = data.find(b"XALZ")
print(f"First XALZ at: {idx}")
sample = data[idx:idx+40]
print("Hex:", sample.hex())
print("ASCII:", sample)
