import dnfile
from pathlib import Path

extracted = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls")
for f in sorted(extracted.glob("*.dll")):
    try:
        pe = dnfile.dnPE(str(f))
        if hasattr(pe, "net") and hasattr(pe.net, "mdtables") and hasattr(pe.net.mdtables, "Assembly"):
            asm = pe.net.mdtables.Assembly[0]
            print(f"{f.name:25} -> {asm.Name}")
    except Exception:
        pass
