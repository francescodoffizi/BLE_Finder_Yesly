import dnfile
from pathlib import Path

extracted = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls")
mapping = {}
for f in extracted.glob("*.dll"):
    try:
        pe = dnfile.dnPE(str(f))
        if hasattr(pe, "net") and hasattr(pe.net, "mdtables") and hasattr(pe.net.mdtables, "Assembly"):
            asm = pe.net.mdtables.Assembly[0]
            name = str(asm.Name)
            mapping[name] = f.name
            if "Finder" in name:
                print(f"Assembly: {name:<30} File: {f.name}")
    except Exception:
        pass
