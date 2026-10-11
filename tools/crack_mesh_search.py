from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
import struct

gw_key = bytes.fromhex("00112233445566778899aabbccddeeff")
tv_key = bytes.fromhex("00112233445566778899aabbccddeeff")
balcone_key = bytes.fromhex("00112233445566778899aabbccddeeff")

# Target 1: Luce TV Seq EF (239) Cmd 03 -> 1c 9e cd 44
# Target 2: Balcone Seq F7 (247) Cmd 03 -> ba 99 45 ee

tv_mic = bytes.fromhex("1c9ecd44")
balcone_mic = bytes.fromhex("ba9945ee")

# Let's brute force the plain structure of the AES-128 block:
# Block size = 16 bytes.
# In AES-ECB / AES-CBC / CMAC:
# What 16-byte block yields AES_Encrypt(k, block)[:4] == mic?
# Let's check with AES Decrypt on the 4-byte prefix!
# Since AES is a block cipher, we can decrypt any 16-byte ciphertext [mic, b1, b2, ... b12]!
# But testing 2^(8*12) is impossible.
# HOWEVER: if the MIC is a CMAC or CBC-MAC over a short message:

keys_to_test = [
    ("Gateway", gw_key, [("TV", tv_mic, 0xEF, 3, bytes.fromhex("8507")), ("Balcone", balcone_mic, 0xF7, 3, bytes.fromhex("560a"))]),
    ("DevKey", None, [("TV", tv_mic, 0xEF, 3, bytes.fromhex("8507")), ("Balcone", balcone_mic, 0xF7, 3, bytes.fromhex("560a"))]),
]

print("Testing CMAC variations...")
for kname, k, targets in keys_to_test:
    for tname, mic, seq, cmd, addr in targets:
        actual_key = k if k else (tv_key if tname == "TV" else balcone_key)
        # Try constructing variations of data:
        for seq_format in [bytes([seq]), struct.pack("<H", seq), struct.pack(">H", seq), struct.pack("<I", seq), struct.pack(">I", seq)]:
            for cmd_format in [bytes([cmd]), bytes([0x61, 0x0E, 0x00, cmd]), bytes([cmd, 0x00, 0x0E, 0x61])]:
                for addr_format in [addr, addr[::-1], b"\x00" + addr, addr + b"\x00"]:
                    for pad in [b"", b"\x00", b"\x01", b"\x00" * 4, b"\x00" * 8]:
                        for order in [
                            seq_format + cmd_format + addr_format + pad,
                            cmd_format + seq_format + addr_format + pad,
                            addr_format + seq_format + cmd_format + pad,
                            addr_format + cmd_format + seq_format + pad,
                        ]:
                            # CMAC
                            c = cmac.CMAC(algorithms.AES(actual_key))
                            c.update(order)
                            tag = c.finalize()
                            if tag[:4] == mic or tag[:4] == mic[::-1] or tag[-4:] == mic or tag[-4:] == mic[::-1]:
                                print(f"[MATCH CMAC!] {kname} {tname} data={order.hex()}")
                                exit(0)
print("No direct CMAC match in search space.")
