import zipfile
from pathlib import Path

p = Path("/root/workspace/BLE_Finder_Yesly/unpacked_apk/config.arm64_v8a.apk")
with zipfile.ZipFile(p, 'r') as z:
    for name in z.namelist():
        if "finder" in name.lower() or "yesly" in name.lower() or "ble" in name.lower() or "iot" in name.lower() or "bluetooth" in name.lower():
            print(name)
