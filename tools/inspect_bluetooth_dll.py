import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

print(f"Inspecting {dll_path.name}:")
if hasattr(pe, "net"):
    md = pe.net.mdtables
    if hasattr(md, "TypeDef"):
        print("TypeDef classes:")
        for row in md.TypeDef:
            ns = str(row.TypeNamespace)
            name = str(row.TypeName)
            if any(k in name.lower() for k in ["mesh", "command", "crypto", "packet", "security", "frame", "auth", "mic", "aes", "ble", "yesly", "relay", "sender", "adv"]):
                print(f"  {ns}.{name}")
