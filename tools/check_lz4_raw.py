import lz4.block
from pathlib import Path

so_path = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so")
data = so_path.read_bytes()

idx = 34227
chunk = data[idx+12:idx+12+4000]
print("Chunk length:", len(chunk))
try:
    d = lz4.block.decompress(chunk, uncompressed_size=0x038400)
    print("Decompressed length:", len(d))
    print("Header:", d[:10])
except Exception as e:
    print("Error:", e)
