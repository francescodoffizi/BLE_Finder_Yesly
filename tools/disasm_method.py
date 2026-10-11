import dnfile
from pathlib import Path

# Disassemble IL instructions from MethodDef
dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for row in pe.net.mdtables.MethodDef:
    name = str(row.Name)
    if name in ["GenerateSwitchOnCommand", "GenerateSwitchOffCommand", "GenerateSequenceSetCommand"]:
        print(f"\n================ Method: {name} ================")
        rva = row.Rva
        if rva:
            # Read method body
            offset = pe.get_offset_from_rva(rva)
            raw = pe.__data__[offset:offset+200]
            print("Hex:", raw.hex())
