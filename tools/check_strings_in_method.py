import dnfile
from pathlib import Path

dll_path = Path("/root/workspace/BLE_Finder_Yesly/extracted_dlls/FinderCommon.Bluetooth.dll")
pe = dnfile.dnPE(str(dll_path))

# Check UserString heap (0x70 tokens used in ldstr instructions)
# The opcode '72 xx xx xx 70' is ldstr!
ldstr_tokens = [0x0017fc, 0x001806, 0x001810, 0x00181a, 0x001824, 0x00182e]
if hasattr(pe.net, "user_strings"):
    for t in ldstr_tokens:
        try:
            s = pe.net.user_strings.get(t)
            print(f"Token 0x{t:X} string: '{s.value}'")
        except Exception as e:
            print(f"Token 0x{t:X} error: {e}")
