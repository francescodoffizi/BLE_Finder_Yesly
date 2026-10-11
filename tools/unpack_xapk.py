import zipfile
from pathlib import Path

xapk_path = Path("/root/workspace/01_Projects/BLE_Finder_Yesly/Finder+You_1.4.5_APKPure.xapk")
out_dir = Path("/root/workspace/BLE_Finder_Yesly/unpacked_apk")
out_dir.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(xapk_path, 'r') as z:
    z.printdir()
    z.extractall(out_dir)

print(f"Extracted XAPK to {out_dir}")
