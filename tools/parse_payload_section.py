import struct
import lz4.block
from pathlib import Path

so_data = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so").read_bytes()
payload = so_data[0x4000:0x4000+0xc7180b]

# Check the beginning of the payload
print("Payload start (hex):", payload[:40].hex())
print("Payload start (ASCII):", payload[:40])

# In .NET 6/7/8/9 Android assembly store:
# Header:
# uint32 magic = 0x58414241 ('XABA') or 0x41424158
# uint32 version
# uint32 entry_count
# entries: [uint32 data_offset, uint32 data_size, ...]
magic, version, count = struct.unpack("<III", payload[:12])
print(f"Magic: 0x{magic:08X} (ASCII: {payload[:4]}), Version: {version}, Count: {count}")
