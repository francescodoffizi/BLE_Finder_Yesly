import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')

for n in pe.net.mdtables.NestedClass:
    if str(n.EnclosingClass.row.TypeName) == 'DeviceCommandHandler' and str(n.NestedClass.row.TypeName) == '<Handle>d__5':
        t = n.NestedClass.row
        break

m = [x for x in t.MethodList if str(x.row.Name) == 'MoveNext'][0]
rva = m.row.Rva
offset = pe.get_offset_from_rva(rva)
code = pe.__data__[offset+12:offset+12+4854]

# Print calls and field accesses in the first 0x300 bytes of MoveNext
for i in range(0, min(len(code)-5, 0x400)):
    if code[i] in [0x28, 0x6F, 0x7B]:
        tok = int.from_bytes(code[i+1:i+5], "little")
        table = tok >> 24
        row_id = (tok & 0xFFFFFF) - 1
        name = ""
        try:
            if table == 4: name = f"Field: {pe.net.mdtables.Field[row_id].Name}"
            elif table == 6: name = f"MethodDef: {pe.net.mdtables.MethodDef[row_id].Name}"
            elif table == 10: name = f"MemberRef: {pe.net.mdtables.MemberRef[row_id].Name}"
            if name: print(f"{i:04X}: {name}")
        except Exception:
            pass
