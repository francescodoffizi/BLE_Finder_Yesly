import zipfile
from pathlib import Path

for apk_file in ["com.findernet.FinderYou.apk", "config.arm64_v8a.apk"]:
    p = Path(f"/root/workspace/BLE_Finder_Yesly/unpacked_apk/{apk_file}")
    with zipfile.ZipFile(p, 'r') as z:
        for name in z.namelist():
            if name.endswith(".dll") or "assemblies" in name or name.endswith(".so"):
                print(f"[{apk_file}] {name}")
