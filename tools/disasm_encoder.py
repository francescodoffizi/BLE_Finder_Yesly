import dnfile
from pathlib import Path

# Find BleDeviceEncoder in FinderCommon.Data.dll
dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Data.dll")
pe = dnfile.dnPE(str(dll_path))

for cls in pe.net.mdtables.TypeDef:
    cname = str(cls.TypeName)
    if "Encoder" in cname or "BleDevice" in cname or "Packet" in cname or "Security" in cname:
        print(f"Class: {cls.TypeNamespace}.{cname}")
        for m in cls.MethodList:
            print(f"   -> Method: {m.row.Name}")
