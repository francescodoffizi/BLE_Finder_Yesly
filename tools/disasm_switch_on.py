import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderCommon.Bluetooth.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == 'BluetoothAdvSetGenerator'][0]
for m in t.MethodList:
    if 'Switch' in str(m.row.Name) or 'ButtonClick' in str(m.row.Name) or 'Command' in str(m.row.Name):
        print(f"Method: {m.row.Name}")
        off = pe.get_offset_from_rva(m.row.Rva)
        print(pe.__data__[off:off+100].hex())
