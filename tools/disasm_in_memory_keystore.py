import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == 'InMemoryKeyStore'][0]
for m in t.MethodList:
    print(f"Method: {m.row.Name}")
    rva = m.row.Rva
    if not rva: continue
    off = pe.get_offset_from_rva(rva)
    code = pe.__data__[off+12:off+12+200]
    for i in range(len(code)-5):
        if code[i] in [0x28, 0x6F]:
            tok = int.from_bytes(code[i+1:i+5], "little")
            table = tok >> 24
            row_id = (tok & 0xFFFFFF) - 1
            try:
                name = ""
                if table == 6: name = pe.net.mdtables.MethodDef[row_id].Name
                elif table == 10: name = pe.net.mdtables.MemberRef[row_id].Name
                print(f"  Calls {name}")
            except Exception:
                pass
