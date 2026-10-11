import zipfile

for apk in ["com.findernet.FinderYou.apk", "config.arm64_v8a.apk"]:
    with zipfile.ZipFile(f"/root/workspace/BLE_Finder_Yesly/unpacked_apk/{apk}") as z:
        for name in z.namelist():
            if "arm64" in name:
                info = z.getinfo(name)
                if "Finder" in name:
                    print(f"[{apk}] {name} ({info.file_size} bytes)")
