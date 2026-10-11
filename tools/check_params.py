import dnfile

pe = dnfile.dnPE('extracted_real_dlls/FinderYou.Webapp.dll')
t = [x for x in pe.net.mdtables.TypeDef if str(x.TypeName) == 'BluetoothAdvSetGenerator'][0]
for m in t.MethodList:
    if str(m.row.Name) in ['GenerateSwitchOnCommand', 'GenerateDevice13xxButtonClick']:
        print(f"Method: {m.row.Name}")
        for p in m.row.ParamList:
            print(f"  Param: {p.row.Name}")
