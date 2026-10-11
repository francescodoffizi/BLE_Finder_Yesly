import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')
target_off = 0x28604

for t in pe.net.mdtables.TypeDef:
    for m in t.MethodList:
        if not m.row.Rva: continue
        off = pe.get_offset_from_rva(m.row.Rva)
        header = pe.__data__[off]
        flags = header & 3
        if flags == 2:
            code_size = header >> 2
            code_start = off + 1
        else:
            code_size = int.from_bytes(pe.__data__[off+4:off+8], "little")
            code_start = off + 12
        if code_start <= target_off < code_start + code_size:
            print(f"FOUND: {t.TypeName}.{m.row.Name} (Rva: 0x{m.row.Rva:X})")
