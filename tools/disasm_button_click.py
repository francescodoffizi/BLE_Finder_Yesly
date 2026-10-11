import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for row in pe.net.mdtables.MethodDef:
    name = str(row.Name)
    if name == "GenerateDevice13xxButtonClick":
        rva = row.Rva
        offset = pe.get_offset_from_rva(rva)
        header = pe.__data__[offset]
        flags = header & 3
        if flags == 2:
            code_size = header >> 2
            code = pe.__data__[offset+1:offset+1+code_size]
        else:
            code_size = int.from_bytes(pe.__data__[offset+4:offset+8], "little")
            code = pe.__data__[offset+12:offset+12+code_size]
        print(f"Method {name}: Code size: {code_size} bytes")
        for i in range(len(code)-4):
            if code[i] == 0x28:
                token = int.from_bytes(code[i+1:i+5], "little")
                table = token >> 24
                row_id = token & 0xFFFFFF
                if table == 6:
                    print("  Calls MethodDef:", pe.net.mdtables.MethodDef[row_id-1].Name)
                elif table == 10:
                    print("  Calls MemberRef:", pe.net.mdtables.MemberRef[row_id-1].Name)
