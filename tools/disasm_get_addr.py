import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Data.dll')
# Token was 0x06000A1E -> MethodDef row 0xA1E - 1 = 0xA1D
m = pe.net.mdtables.MethodDef[0xA1D]
print(f"Method: {m.Name}")
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
print("Code hex:", code.hex())
