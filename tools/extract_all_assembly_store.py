import struct
import lz4.block
from pathlib import Path

# Let's inspect libassembly-store.so structure carefully:
# Often it has an index at the beginning or end listing all assemblies and their byte ranges!
so_path = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so")
data = so_path.read_bytes()

# Look for strings ending in .dll
pos = 0
dlls = []
for m in [b"FinderCommon.Data.dll", b"FinderCommon.Bluetooth.dll", b"FinderHome.Grpc.Common.dll"]:
    idx = data.find(m)
    print(f"String '{m.decode()}' found at offset {idx}")

