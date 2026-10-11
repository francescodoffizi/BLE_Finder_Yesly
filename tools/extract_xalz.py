import struct
import lz4.block
from pathlib import Path

so_path = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so")
data = so_path.read_bytes()

out_dir = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls")
out_dir.mkdir(parents=True, exist_ok=True)

pos = 0
count = 0
while True:
    idx = data.find(b"XALZ", pos)
    if idx == -1:
        break
    header_index, uncompressed_size = struct.unpack("<II", data[idx+4:idx+12])
    # The compressed data starts at idx+12
    # Check if uncompressed size is reasonable (e.g. up to 20MB)
    if 100 < uncompressed_size < 30_000_000:
        try:
            # Let's try decompressed slice
            decomp = lz4.block.decompress(data[idx+12:idx+12+uncompressed_size], uncompressed_size=uncompressed_size)
            if decomp.startswith(b"MZ"):
                count += 1
                out_file = out_dir / f"assembly_{count}_{header_index}.dll"
                out_file.write_bytes(decomp)
                print(f"Extracted #{count}: {out_file.name} (uncompressed: {uncompressed_size} bytes)")
        except Exception:
            pass
    pos = idx + 4

print(f"Total DLLs extracted: {count}")
