import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for a in pe.net.mdtables.AssemblyRef:
    print("AssemblyRef:", a.Name)
