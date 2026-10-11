import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == '<LoadDeviceKey>d__81'][0]
m = [x for x in t.MethodList if str(x.row.Name) == 'MoveNext'][0]
rva = m.row.Rva
offset = pe.get_offset_from_rva(rva)
code = pe.__data__[offset+12:offset+12+1000]

OPCODES = {
    0x02: "ldarg.0", 0x06: "ldloc.0", 0x07: "ldloc.1", 0x08: "ldloc.2", 0x09: "ldloc.3",
    0x14: "ldnull", 0x16: "ldc.i4.0", 0x17: "ldc.i4.1", 0x28: "call", 0x2A: "ret",
    0x6F: "callvirt", 0x7B: "ldfld", 0x7D: "stfld", 0x80: "stsfld"
}

pc = 0x0000
while pc < 0x00C0:
    b = code[pc]
    op = OPCODES.get(b, f"0x{b:02X}")
    info = f"{pc:04X}: {op}"
    if b in [0x28, 0x6F, 0x7B, 0x7D, 0x80]:
        tok = int.from_bytes(code[pc+1:pc+5], "little")
        table = tok >> 24
        row_id = (tok & 0xFFFFFF) - 1
        name = ""
        try:
            if table == 4: name = pe.net.mdtables.Field[row_id].Name
            elif table == 6: name = pe.net.mdtables.MethodDef[row_id].Name
            elif table == 10: name = pe.net.mdtables.MemberRef[row_id].Name
        except Exception:
            pass
        info += f" ({name})"
        pc += 5
    elif b in [0x1F, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x2B, 0x2C, 0x2D, 0x2E]:
        info += f" 0x{code[pc+1]:02X}"
        pc += 2
    else:
        pc += 1
    print(info)
