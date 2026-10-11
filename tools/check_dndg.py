import dnfile
from pathlib import Path

for name in ["assembly_102.dll", "assembly_103.dll", "assembly_104.dll"]:
    p = Path(f"/root/workspace/BLE_Finder_Yesly/extracted_dlls/{name}")
    try:
        pe = dnfile.dnPE(str(p))
        if hasattr(pe, "net") and hasattr(pe.net, "mdtables"):
            asm = pe.net.mdtables.Assembly[0]
            print(f"{name} -> Assembly Name: {asm.Name}")
    except Exception as e:
        print(f"{name} -> err: {e}")
