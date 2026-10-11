import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

for r in pe.net.mdtables.MemberRef:
    if str(r.Name) == "CreateWithKey":
        parent = r.Class.row
        print(f"Parent type: {type(parent)} name={getattr(parent, 'TypeName', '')} ns={getattr(parent, 'TypeNamespace', '')}")
        # If TypeRef:
        if hasattr(parent, "ResolutionScope"):
            scope = parent.ResolutionScope.row
            print(f"Scope: {getattr(scope, 'Name', '')}")
