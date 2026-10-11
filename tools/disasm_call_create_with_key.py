import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Bluetooth.dll')

for t in pe.net.mdtables.TypeDef:
    for m in t.MethodList:
        if not m.row.Rva: continue
        off = pe.get_offset_from_rva(m.row.Rva)
        code = pe.__data__[off:off+400]
        # Look for call to CreateWithKey (token)
        # Let's search MemberRef for CreateWithKey
        for r_idx, r in enumerate(pe.net.mdtables.MemberRef):
            if str(r.Name) == 'CreateWithKey':
                tok = (0x0A << 24) | (r_idx + 1)
                tok_b = bytes([0x28, tok & 0xFF, (tok >> 8) & 0xFF, (tok >> 16) & 0xFF, (tok >> 24) & 0xFF])
                if tok_b in code:
                    pos = code.find(tok_b)
                    print(f"Found call in {t.TypeName}.{m.row.Name} at offset {pos}:")
                    pre = code[max(0, pos-30):pos]
                    print("Preceding bytes:", pre.hex())
