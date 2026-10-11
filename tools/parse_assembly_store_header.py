import struct
import lz4.block
from pathlib import Path

so_path = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so")
data = so_path.read_bytes()

# The assembly store header in modern .NET Android:
# Header: magic 'XABA' or 4-byte magic
# Let's inspect the first 256 bytes of libassembly-store.so
print("First 64 bytes of libassembly-store.so:")
print(data[:64].hex())
print("ASCII:", data[:64])
