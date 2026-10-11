import zipfile
from pathlib import Path

apk_path = Path("/root/workspace/BLE_Finder_Yesly/unpacked_apk/com.findernet.FinderYou.apk")
with zipfile.ZipFile(apk_path, 'r') as z:
    for name in z.namelist():
        if "assemblies" in name or name.endswith(".blob"):
            print("Main APK:", name)
