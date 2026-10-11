import struct
import lz4.block
from pathlib import Path

# Xamarin XALZ format:
# Byte 0..3: 'XALZ'
# Byte 4..7: Header index (CRC32 or magic)
# Byte 8..11: Uncompressed length
# Byte 12..end: LZ4 block

def decompress_xalz(data):
    if not data.startswith(b"XALZ"):
        return None
    header_idx, uncompressed_len = struct.unpack("<II", data[4:12])
    payload = data[12:]
    return lz4.block.decompress(payload, uncompressed_size=uncompressed_len)

# Let's inspect where the block ends!
so_data = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so").read_bytes()
idx1 = so_data.find(b"XALZ")
idx2 = so_data.find(b"XALZ", idx1 + 4)
print(f"Block 1 from {idx1} to {idx2} (len: {idx2 - idx1})")

block1 = so_data[idx1:idx2]
uncompressed = decompress_xalz(block1)
if uncompressed:
    print("SUCCESS! Decompressed block 1! Size:", len(uncompressed))
    print("Header:", uncompressed[:20])
else:
    print("Failed to decompress block 1 directly.")
