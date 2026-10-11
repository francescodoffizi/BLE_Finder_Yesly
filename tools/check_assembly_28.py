import dnfile
from pathlib import Path

p = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/assembly_28.dll")
pe = dnfile.dnPE(str(p))

asm = pe.net.mdtables.Assembly[0]
print(f"assembly_28.dll IS: {asm.Name}!")

for t in pe.net.mdtables.TypeDef:
    if "Encoder" in str(t.TypeName) or "Ble" in str(t.TypeName):
        print(f"Class: {t.TypeNamespace}.{t.TypeName}")
        for m in t.MethodList:
            print(f"  Method: {m.row.Name}")
