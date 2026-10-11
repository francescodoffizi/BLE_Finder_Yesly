import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for cls in pe.net.mdtables.TypeDef:
    name = str(cls.TypeName)
    if "ButtonClick" in name or "13xx" in name or "15xx" in name or "Generator" in name:
        print(f"Type: {cls.TypeNamespace}.{name}")
        for m in cls.MethodList:
            print(f"    Method: {m.row.Name}")
