import dnfile
from pathlib import Path

# Extract the full byte stream of GenerateSwitchOnCommand
dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for row in pe.net.mdtables.MethodDef:
    name = str(row.Name)
    if name == "GenerateSwitchOnCommand":
        rva = row.Rva
        offset = pe.get_offset_from_rva(rva)
        # Read header: fat or tiny header
        header = pe.__data__[offset]
        flags = header & 3
        if flags == 2: # tiny
            code_size = header >> 2
            code = pe.__data__[offset+1:offset+1+code_size]
        else: # fat
            code_size = int.from_bytes(pe.__data__[offset+4:offset+8], "little")
            header_size = (header >> 4) * 4
            code = pe.__data__[offset+12:offset+12+code_size]
        print(f"Code size: {code_size} bytes")
        
        # Search all MemberRefs/MethodDefs called in this code
        # Format of call: 0x28 <4 bytes token>
        for i in range(len(code)-4):
            if code[i] == 0x28:
                token = int.from_bytes(code[i+1:i+5], "little")
                table = token >> 24
                row_id = token & 0xFFFFFF
                if table == 6: # MethodDef
                    target_name = pe.net.mdtables.MethodDef[row_id-1].Name
                    print(f"Calls MethodDef: {target_name}")
                elif table == 10: # MemberRef
                    target_name = pe.net.mdtables.MemberRef[row_id-1].Name
                    print(f"Calls MemberRef: {target_name}")
