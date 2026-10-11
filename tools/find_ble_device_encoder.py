import dnfile
from pathlib import Path

extracted = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls")
for f in extracted.glob("*.dll"):
    try:
        pe = dnfile.dnPE(str(f))
        if hasattr(pe, "net") and hasattr(pe.net, "mdtables") and hasattr(pe.net.mdtables, "TypeDef"):
            for t in pe.net.mdtables.TypeDef:
                if str(t.TypeName) == "BleDeviceEncoder":
                    print(f"FOUND BleDeviceEncoder in {f.name} (Namespace: {t.TypeNamespace})!")
                    for m in t.MethodList:
                        print(f"   -> Method: {m.row.Name}")
    except Exception:
        pass
