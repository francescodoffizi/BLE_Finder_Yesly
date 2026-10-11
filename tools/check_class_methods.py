import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for cls in pe.net.mdtables.TypeDef:
    name = str(cls.TypeName)
    if name == "BluetoothAdvSetGenerator":
        print("Found BluetoothAdvSetGenerator!")
        for m in cls.MethodList:
            print(f" -> {m.row.Name}")
