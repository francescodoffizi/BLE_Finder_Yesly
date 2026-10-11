import dnfile
from pathlib import Path

p = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/assembly_102.dll")
pe = dnfile.dnPE(str(p))

print(f"Classes in {p.name} (Dndg.Bluetooth):")
for t in pe.net.mdtables.TypeDef:
    print(f"  {t.TypeNamespace}.{t.TypeName}")
    for m in t.MethodList:
        print(f"     -> {m.row.Name}")
