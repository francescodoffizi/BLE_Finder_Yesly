import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')

# Find <Handle>d__5 nested in DeviceCommandHandler
for n in pe.net.mdtables.NestedClass:
    if str(n.EnclosingClass.row.TypeName) == 'DeviceCommandHandler' and str(n.NestedClass.row.TypeName) == '<Handle>d__5':
        t = n.NestedClass.row
        break

m = [x for x in t.MethodList if str(x.row.Name) == 'MoveNext'][0]
rva = m.row.Rva
offset = pe.get_offset_from_rva(rva)
header = pe.__data__[offset]
flags = header & 3
if flags == 2:
    code_size = header >> 2
    code = pe.__data__[offset+1:offset+1+code_size]
    start_off = offset + 1
else:
    code_size = int.from_bytes(pe.__data__[offset+4:offset+8], "little")
    code = pe.__data__[offset+12:offset+12+code_size]
    start_off = offset + 12

rel_off = 0x28604 - start_off
print(f"Code size: {code_size}, target rel offset: 0x{rel_off:X}")

# Print calls around rel_off
for i in range(max(0, rel_off - 100), min(len(code)-5, rel_off + 200)):
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
