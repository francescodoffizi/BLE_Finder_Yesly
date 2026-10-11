import dnfile
from pathlib import Path

# In FinderCommon.Bluetooth.dll:
# MoveNext in <GenerateDevice13xxButtonClick>d__4 calls CreateWithKey
# Let's inspect the exact IL instructions around that call!
dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for cls in pe.net.mdtables.TypeDef:
    if "GenerateDevice13xxButtonClick" in str(cls.TypeName):
        for m in cls.MethodList:
            if str(m.row.Name) == "MoveNext":
                rva = m.row.Rva
                offset = pe.get_offset_from_rva(rva)
                header = pe.__data__[offset]
                flags = header & 3
                if flags == 2:
                    code_size = header >> 2
                    code = pe.__data__[offset+1:offset+1+code_size]
                else:
                    code_size = int.from_bytes(pe.__data__[offset+4:offset+8], "little")
                    code = pe.__data__[offset+12:offset+12+code_size]
                
                print("IL code bytes around CreateWithKey:")
                for i in range(len(code)-5):
                    if code[i] == 0x28:
                        token = int.from_bytes(code[i+1:i+5], "little")
                        name = ""
                        table = token >> 24
                        row_id = token & 0xFFFFFF
                        if table == 10:
                            name = pe.net.mdtables.MemberRef[row_id-1].Name
                        elif table == 6:
                            name = pe.net.mdtables.MethodDef[row_id-1].Name
                        if name == "CreateWithKey":
                            # Print 40 bytes before this call!
                            pre = code[max(0, i-40):i]
                            print("Preceding opcodes (hex):", pre.hex())
