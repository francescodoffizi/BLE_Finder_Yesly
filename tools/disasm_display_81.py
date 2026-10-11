import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')
t = [x for x in pe.net.mdtables.TypeDef if '<>c__DisplayClass81_0' in str(x.TypeName)][0]
m = t.MethodList[0] # <LoadDeviceKey>b__0
rva = m.row.Rva
offset = pe.get_offset_from_rva(rva)
code = pe.__data__[offset+12:offset+12+400]

for i in range(len(code)-5):
    if code[i] in [0x28, 0x6F, 0x7B]:
        tok = int.from_bytes(code[i+1:i+5], "little")
        table = tok >> 24
        row_id = (tok & 0xFFFFFF) - 1
        name = ""
        try:
            if table == 4: name = f"Field: {pe.net.mdtables.Field[row_id].Name}"
            elif table == 6: name = f"MethodDef: {pe.net.mdtables.MethodDef[row_id].Name}"
            elif table == 10: name = f"MemberRef: {pe.net.mdtables.MemberRef[row_id].Name}"
            print(f"{i:04X}: {name}")
        except Exception:
            pass
