import zipfile
from pathlib import Path

apk_path = Path("/root/workspace/BLE_Finder_Yesly/unpacked_apk/config.arm64_v8a.apk")
with zipfile.ZipFile(apk_path, 'r') as z:
    z.extract("lib/arm64-v8a/libassembly-store.so", "/root/workspace/BLE_Finder_Yesly/")

print("Extracted libassembly-store.so successfully!")
