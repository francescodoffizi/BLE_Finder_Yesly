import dnfile

pe = dnfile.dnPE('extracted_real_dlls/BouncyCastle.Crypto.dll')
t = [x for x in pe.net.mdtables.TypeDef if 'CcmBlockCipher' in str(x.TypeName)][0]
m = [x for x in t.MethodList if str(x.row.Name) == 'CalculateMac'][0]
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

print(f"Code size: {code_size}")
for i in range(len(code)-5):
    if code[i] in [0x28, 0x6F]:
        tok = int.from_bytes(code[i+1:i+5], "little")
        table = tok >> 24
        row_id = (tok & 0xFFFFFF) - 1
        name = ""
        cls = ""
        try:
            if table == 6: name = pe.net.mdtables.MethodDef[row_id].Name
            elif table == 10:
                name = pe.net.mdtables.MemberRef[row_id].Name
                cls = getattr(getattr(pe.net.mdtables.MemberRef[row_id].Class, 'row', None), 'TypeName', None)
            print(f"{i:04X}: Call {name} on {cls}")
        except Exception:
            pass
