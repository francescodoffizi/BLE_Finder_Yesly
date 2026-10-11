import zipfile
from pathlib import Path

apk_path = Path("/root/workspace/BLE_Finder_Yesly/unpacked_apk/config.arm64_v8a.apk")
with zipfile.ZipFile(apk_path, 'r') as z:
    for name in z.namelist():
        if "assembly" in name:
            info = z.getinfo(name)
            print(f"Assembly store: {name} (size: {info.file_size} bytes)")
