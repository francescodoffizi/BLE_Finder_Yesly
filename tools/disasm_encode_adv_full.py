import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Data.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == 'BleDeviceEncoder'][0]
m = [x for x in t.MethodList if str(x.row.Name) == 'EncodeInputBufferForAdv'][0]
rva = m.row.Rva
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
    0x00: "nop", 0x01: "break", 0x02: "ldarg.0", 0x03: "ldarg.1", 0x04: "ldarg.2", 0x05: "ldarg.3",
    0x06: "ldloc.0", 0x07: "ldloc.1", 0x08: "ldloc.2", 0x09: "ldloc.3", 
    0x0A: "stloc.0", 0x0B: "stloc.1", 0x0C: "stloc.2", 0x0D: "stloc.3",
    0x0E: "ldarg.s", 0x0F: "ldarga.s", 0x10: "starg.s", 0x11: "ldloc.s", 0x12: "ldloca.s", 0x13: "stloc.s",
    0x14: "ldnull", 0x15: "ldc.i4.m1", 0x16: "ldc.i4.0", 0x17: "ldc.i4.1", 0x18: "ldc.i4.2", 0x19: "ldc.i4.3",
    0x1A: "ldc.i4.4", 0x1B: "ldc.i4.5", 0x1C: "ldc.i4.6", 0x1D: "ldc.i4.7", 0x1E: "ldc.i4.8",
    0x1F: "ldc.i4.s", 0x20: "ldc.i4", 0x25: "dup", 0x26: "pop", 0x28: "call", 0x29: "calli", 0x2A: "ret",
    0x2B: "br.s", 0x2C: "brfalse.s", 0x2D: "brtrue.s", 0x2E: "beq.s", 0x2F: "bge.s", 0x30: "bgt.s",
    0x31: "ble.s", 0x32: "blt.s", 0x33: "bne.un.s", 0x38: "br", 0x39: "brfalse", 0x3A: "brtrue",
    0x3B: "beq", 0x58: "add", 0x59: "sub", 0x5A: "mul", 0x5B: "div", 0x5E: "and", 0x5F: "or", 0x60: "xor",
    0x61: "shl", 0x62: "shr", 0x6F: "callvirt", 0x72: "newobj", 0x73: "newarr", 0x74: "ldlen",
    0x7B: "ldfld", 0x7C: "ldflda", 0x7D: "stfld", 0x7E: "ldsfld", 0x7F: "ldsflda", 0x80: "stsfld",
    0x8C: "box", 0x8D: "newarr", 0x8E: "ldelem.u1", 0x90: "ldelem.u2", 0x92: "ldelem.i4", 0x94: "ldelem.i8",
    0x96: "ldelem.r4", 0x97: "ldelem.r8", 0x9C: "stelem.i1", 0x9D: "stelem.i2", 0x9E: "stelem.i4",
    0xA3: "conv.u1", 0xA4: "conv.u2", 0xD0: "ldtoken"
}

def resolve_token(token):
    table = token >> 24
    row = (token & 0xFFFFFF) - 1
    try:
        if table == 1: return f"TypeRef:{pe.net.mdtables.TypeRef[row].TypeName}"
        if table == 2: return f"TypeDef:{pe.net.mdtables.TypeDef[row].TypeName}"
        if table == 4: return f"Field:{pe.net.mdtables.Field[row].Name}"
        if table == 6: return f"MethodDef:{pe.net.mdtables.MethodDef[row].Name}"
        if table == 10: return f"MemberRef:{pe.net.mdtables.MemberRef[row].Name} ({getattr(getattr(pe.net.mdtables.MemberRef[row].Class, 'row', None), 'TypeName', None)})"
    except Exception:
        pass
    return f"Token:0x{token:08X}"

pc = 0
while pc < len(code):
    b = code[pc]
    op = OPCODES.get(b, f"0x{b:02X}")
    info = f"{pc:04X}: {op}"
    if b in [0x28, 0x6F, 0x72, 0x73, 0x7B, 0x7D, 0x7E, 0x80, 0xD0]:
        tok = int.from_bytes(code[pc+1:pc+5], "little")
        info += f" ({resolve_token(tok)})"
        pc += 5
    elif b in [0x1F, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33]:
        info += f" 0x{code[pc+1]:02X}"
        pc += 2
    elif b in [0x20, 0x38, 0x39, 0x3A, 0x3B]:
        imm = int.from_bytes(code[pc+1:pc+5], "little", signed=True)
        info += f" {imm}"
        pc += 5
    elif b == 0x8D:
        tok = int.from_bytes(code[pc+1:pc+5], "little")
        info += f" ({resolve_token(tok)})"
        pc += 5
    else:
        pc += 1
    print(info)
