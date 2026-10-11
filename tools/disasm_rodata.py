import subprocess
from pathlib import Path

# Extract readelf symbols or sections
res = subprocess.run(["readelf", "-S", "/root/workspace/BLE_Finder_Yesly/lib/arm64-v8a/libassembly-store.so"], capture_output=True, text=True)
print(res.stdout)
