from pathlib import Path

extracted = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls")
target = b"BleDeviceEncoder"

for f in sorted(extracted.glob("*.dll")):
    b = f.read_bytes()
    if target in b:
        print(f"File {f.name} contains 'BleDeviceEncoder' (size: {len(b)} bytes)")
