import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Data.dll')
m = pe.net.mdtables.MethodDef[2758]
rva = m.Rva
offset = pe.get_offset_from_rva(rva)
header = pe.__data__[offset]
flags = header & 3
if flags == 2:
    code_size = header >> 2
    code = pe.__data__[offset+1:offset+1+code_size]
else:
    code_size = int.from_bytes(pe.__data__[offset+4:offset+8], "little")
    code = pe.__data__[offset+12:offset+12+code_size]

OPCODES = {
    0x02: "ldarg.0", 0x14: "ldnull", 0x16: "ldc.i4.0", 0x1F: "ldc.i4.s",
    0x28: "call", 0x2A: "ret", 0x2D: "brtrue.s", 0x6F: "callvirt", 0x7E: "ldsfld"
}

pc = 0
while pc < len(code):
    b = code[pc]
    op = OPCODES.get(b, f"0x{b:02X}")
    info = f"{pc:04X}: {op}"
    if b in [0x1F, 0x2D]:
        info += f" 0x{code[pc+1]:02X}"
        pc += 2
    elif b in [0x28, 0x6F, 0x7E]:
        tok = int.from_bytes(code[pc+1:pc+5], "little")
        table = tok >> 24
        row_id = (tok & 0xFFFFFF) - 1
        name = ""
        if table == 6: name = pe.net.mdtables.MethodDef[row_id].Name
        elif table == 10: name = pe.net.mdtables.MemberRef[row_id].Name
        elif table == 4: name = pe.net.mdtables.Field[row_id].Name
        info += f" ({name})"
        pc += 5
    else:
        pc += 1
    print(info)
