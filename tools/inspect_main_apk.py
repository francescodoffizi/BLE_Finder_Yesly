import zipfile
from pathlib import Path

apk_path = Path("/root/workspace/BLE_Finder_Yesly/unpacked_apk/com.findernet.FinderYou.apk")
with zipfile.ZipFile(apk_path, 'r') as z:
    for name in z.namelist():
        if name.endswith(".so") or "dex" in name or "ble" in name.lower() or "finder" in name.lower() or "mesh" in name.lower() or "assemblies" in name.lower():
            print(name)
