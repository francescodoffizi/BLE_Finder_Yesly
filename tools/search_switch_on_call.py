import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')

# Find MethodDef of GenerateSwitchOnCommand
gen_t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == 'BluetoothAdvSetGenerator'][0]
m_on = [x for x in gen_t.MethodList if str(x.row.Name) == 'GenerateSwitchOnCommand'][0]
idx = gen_t.MethodList.index(m_on)
tok = (0x06 << 24) | gen_t.MethodList[idx].row_index

print(f"Token of GenerateSwitchOnCommand: 0x{tok:08X}")

tok_bytes = bytes([0x28, tok & 0xFF, (tok >> 8) & 0xFF, (tok >> 16) & 0xFF, (tok >> 24) & 0xFF])
tok_virt = bytes([0x6F, tok & 0xFF, (tok >> 8) & 0xFF, (tok >> 16) & 0xFF, (tok >> 24) & 0xFF])

for t in pe.net.mdtables.TypeDef:
    for m in t.MethodList:
        if not m.row.Rva: continue
        off = pe.get_offset_from_rva(m.row.Rva)
        code = pe.__data__[off:off+4000]
        if tok_bytes in code or tok_virt in code:
            print(f"CALL FOUND in {t.TypeName}.{m.row.Name}!")
