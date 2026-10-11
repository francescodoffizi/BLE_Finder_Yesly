import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Data.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == 'BleDeviceEncoder'][0]
m = [x for x in t.MethodList if str(x.row.Name) == 'CreateIV'][0]
rva = m.row.Rva
offset = pe.get_offset_from_rva(rva)
code = pe.__data__[offset+12:offset+12+50]
print("CreateIV bytes (hex):", code.hex())
