import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for r in pe.net.mdtables.MemberRef:
    if str(r.Name) == "CreateWithKey":
        sig = r.Signature.value
        print(f"Signature bytes: {sig.hex()}")
