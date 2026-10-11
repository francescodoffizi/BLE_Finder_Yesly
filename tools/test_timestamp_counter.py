from datetime import datetime, timezone

now = datetime.now(timezone.utc)
epoch_2019 = datetime(2019, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
total_sec = int((now - epoch_2019).total_seconds())

print(f"Total seconds since 2019: {total_sec} (0x{total_sec:08X})")

# Let's inspect the bit operations from GetTimestampCounter:
# 0025: 0x69 (conv.u4 or conv.i4?)
# 0026: dup
# 0027: ldc.i4.s 0x7F (127)
# 0029: and (0x5E is and)
# 002A: stloc.2
# 002B: ldc.i4 2147483520 (0x7FFFFF80)
# 0030: and
# 0031: ldc.i4.1
# 0032: shr
# 0033: ldc.i4 128 (0x80)
# 0038: xor
# 0039: ldloc.2
# 003A: xor
# 003B: ret

sec = total_sec
loc2 = sec & 0x7F
res = (((sec & 0x7FFFFF80) >> 1) ^ 0x80) ^ loc2
print(f"Computed counter: {res} (0x{res:08X})")
print(f"Bytes LE: {res.to_bytes(4, 'little').hex()}")

# What about 2026-10-11 ~09:00?
dt_capture = datetime(2026, 10, 11, 9, 0, 0, tzinfo=timezone.utc)
sec_cap = int((dt_capture - epoch_2019).total_seconds())
print(f"Capture seconds: {sec_cap} (0x{sec_cap:08X})")
