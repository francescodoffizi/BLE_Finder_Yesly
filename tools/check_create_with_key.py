import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for r in pe.net.mdtables.MemberRef:
    name = str(r.Name)
    if "CreateWithKey" in name or "Create" in name or "Encrypt" in name:
        # Check parent class
        print(f"MemberRef: {name} | Class: {r.Class}")
