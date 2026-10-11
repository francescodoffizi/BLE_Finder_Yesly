import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == '<LoadDeviceKey>d__81'][0]
m = [x for x in t.MethodList if str(x.row.Name) == 'MoveNext'][0]
rva = m.row.Rva
offset = pe.get_offset_from_rva(rva)
code = pe.__data__[offset+12:offset+12+1000]

for i in range(len(code)-5):
    if code[i] in [0x28, 0x6F]:
        tok = int.from_bytes(code[i+1:i+5], "little")
        table = tok >> 24
        row_id = (tok & 0xFFFFFF) - 1
        name = ""
        cls = ""
        try:
            if table == 6:
                name = pe.net.mdtables.MethodDef[row_id].Name
            elif table == 10:
                name = pe.net.mdtables.MemberRef[row_id].Name
                cls = getattr(getattr(pe.net.mdtables.MemberRef[row_id].Class, 'row', None), 'TypeName', None)
            print(f"{i:04X}: Call {name} on {cls}")
        except Exception:
            pass
