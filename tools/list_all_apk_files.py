import zipfile
from pathlib import Path

apk_path = Path("/root/workspace/BLE_Finder_Yesly/unpacked_apk/com.findernet.FinderYou.apk")
with zipfile.ZipFile(apk_path, 'r') as z:
    for name in z.namelist():
        if not name.startswith("res/") and not name.startswith("assets/"):
            print("Root/lib:", name)
