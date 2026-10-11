import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Data.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == '<EncodeButton>d__0'][0]
m = [x for x in t.MethodList if str(x.row.Name) == 'MoveNext'][0]
off = pe.get_offset_from_rva(m.row.Rva)
code = pe.__data__[off+12:off+12+0xEE]

for i in range(0x80, 0xBD):
    print(f"{i:04X}: {code[i]:02X}")
