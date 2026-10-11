import dnfile
from pathlib import Path

# In IL, '28 xx xx xx 0a' is a call to a MemberRef (0x0A token) or MethodDef (0x06 token)
# In GenerateSwitchOnCommand:
# 28 46 01 00 06 -> MethodDef token 0x06000146
# 28 8B 01 00 0A -> MemberRef token 0x0A00018B
# 28 8C 01 00 0A -> MemberRef token 0x0A00018C
# 28 8D 01 00 0A -> MemberRef token 0x0A00018D

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

# Check MethodDef 0x146
if hasattr(pe.net.mdtables, "MethodDef"):
    m = pe.net.mdtables.MethodDef[0x146 - 1]
    print(f"MethodDef 0x146: {m.Name}")

# Check MemberRef tokens
if hasattr(pe.net.mdtables, "MemberRef"):
    for tid in [0x18B, 0x18C, 0x18D]:
        m = pe.net.mdtables.MemberRef[tid - 1]
        print(f"MemberRef 0x{tid:X}: {m.Name} (class: {m.Class})")
