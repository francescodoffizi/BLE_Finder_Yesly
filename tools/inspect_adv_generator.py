import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for row in pe.net.mdtables.MethodDef:
    name = str(row.Name)
    if any(k in name.lower() for k in ["generate", "adv", "command", "encrypt", "mic", "mac", "packet", "payload", "13", "15"]):
        print(f"Method: {name}")
