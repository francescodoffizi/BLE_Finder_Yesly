import dnfile
from pathlib import Path

extracted = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls")
for f in extracted.glob("*.dll"):
    try:
        pe = dnfile.dnPE(str(f))
        if hasattr(pe, "net") and hasattr(pe.net, "mdtables") and hasattr(pe.net.mdtables, "MethodDef"):
            for m in pe.net.mdtables.MethodDef:
                if str(m.Name) == "CreateWithKey":
                    asm = pe.net.mdtables.Assembly[0].Name if hasattr(pe.net.mdtables, "Assembly") else ""
                    print(f"FOUND MethodDef CreateWithKey in file: {f.name} (Assembly: {asm})")
    except Exception:
        pass
