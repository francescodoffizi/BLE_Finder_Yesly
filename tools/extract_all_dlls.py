import struct
import lz4.block
from pathlib import Path

so_path = Path("/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so")
so_data = so_path.read_bytes()

out_dir = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls")
out_dir.mkdir(parents=True, exist_ok=True)

# Find all XALZ offsets
offsets = []
pos = 0
while True:
    idx = so_data.find(b"XALZ", pos)
    if idx == -1:
        break
    offsets.append(idx)
    pos = idx + 4

offsets.append(len(so_data))
print(f"Found {len(offsets)-1} XALZ blocks!")

extracted = 0
for i in range(len(offsets) - 1):
    start = offsets[i]
    end = offsets[i+1]
    block = so_data[start:end]
    header_idx, uncompressed_len = struct.unpack("<II", block[4:12])
    payload = block[12:]
    try:
        decomp = lz4.block.decompress(payload, uncompressed_size=uncompressed_len)
        if decomp.startswith(b"MZ"):
            # Try to identify assembly name from bytes
            dll_name = f"assembly_{i}.dll"
            # Search for assembly name in ASCII
            for match in [b"FinderCommon.Bluetooth", b"FinderCommon.Data", b"FinderHome.Grpc", b"FinderYou.App", b"FinderYou.Webapp"]:
                if match in decomp:
                    dll_name = match.decode() + ".dll"
                    break
            out_file = out_dir / dll_name
            out_file.write_bytes(decomp)
            extracted += 1
            if "Finder" in dll_name:
                print(f"[*] EXTRACTED FINDER DLL: {dll_name} ({len(decomp)} bytes)")
    except Exception as e:
        pass

print(f"Total extracted PE/DLL files: {extracted}")
