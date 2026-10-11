import json
from pathlib import Path
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import struct

keys_file = Path(__file__).parent.parent / "keys.json"
with open(keys_file) as f:
    plant_data = json.load(f)

# Gateway Key & Luce TV Master
gw_key = bytes.fromhex("00112233445566778899aabbccddeeff")
tv_key = bytes.fromhex("00112233445566778899aabbccddeeff")
balcone_key = bytes.fromhex("00112233445566778899aabbccddeeff") # from keys.json for 48fb9007 / 05:61:01:00:56:0A

print("Testing TV target...")
# Notice Seq EF, Cmd 3 -> 1c9ecd44
# Notice Balcone Seq F7, Cmd 3 -> ba9945ee
# If both use the Gateway Key, then the difference must be device address (85 07 vs 56 0A) or key!
