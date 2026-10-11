import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Data.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == 'BleDeviceEncoder'][0]
m = [x for x in t.MethodList if str(x.row.Name) == 'PutUInt32'][0]
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
    0x16: "ldc.i4.0", 0x17: "ldc.i4.1", 0x18: "ldc.i4.2", 0x19: "ldc.i4.3",
    0x1A: "ldc.i4.4", 0x1B: "ldc.i4.5", 0x1C: "ldc.i4.6", 0x1D: "ldc.i4.7", 0x1E: "ldc.i4.8",
    0x1F: "ldc.i4.s", 0x20: "ldc.i4", 0x25: "dup", 0x26: "pop", 0x28: "call", 0x2A: "ret",
    0x2B: "br.s", 0x2C: "brfalse.s", 0x2D: "brtrue.s", 0x2E: "beq.s", 0x31: "ble.s", 0x32: "blt.s",
    0x58: "add", 0x59: "sub", 0x5A: "mul", 0x5B: "div", 0x5E: "and", 0x5F: "or", 0x60: "xor",
    0x61: "shl", 0x62: "shr", 0x6F: "callvirt", 0x8E: "ldelem.u1", 0x9C: "stelem.i1", 0xA3: "conv.u1",
    0xA4: "conv.u2", 0xD2: "conv.u1", 0x91: "ldelem.u1"
}

pc = 0
while pc < len(code):
    b = code[pc]
    op = OPCODES.get(b, f"0x{b:02X}")
    info = f"{pc:04X}: {op}"
    if b in [0x1F, 0x2B, 0x2C, 0x2D, 0x2E]:
        info += f" 0x{code[pc+1]:02X}"
        pc += 2
    elif b in [0x20]:
        imm = int.from_bytes(code[pc+1:pc+5], "little")
        info += f" {imm}"
        pc += 5
    elif b in [0x28, 0x6F, 0x7E]:
        tok = int.from_bytes(code[pc+1:pc+5], "little")
        info += f" (0x{tok:08X})"
        pc += 5
    else:
        pc += 1
    print(info)
