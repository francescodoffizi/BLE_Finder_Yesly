import json
from proto import parse_fields

with open("/root/workspace/plant_dump.bin", "rb") as f:
    data = f.read()

top = parse_fields(data)
plant = parse_fields(top[3][0])

# Captured command packets and their meanings:
# 1. Turn OFF:
#    Seq EF, 61 0E 00, Cmd 03, MIC: 1C 9E CD 44
#    Seq F0, 61 0E 00, Cmd 02, MIC: C6 15 26 56
# 2. Turn ON:
#    Seq F1, 61 0E 00, Cmd 03, MIC: A9 8C CF E3
#    Seq F2, 61 0E 00, Cmd 02, MIC: A1 F2 4A 91
# 3. Turn OFF:
#    Seq F3, 61 0E 00, Cmd 03, MIC: A4 13 DC 50
#    Seq F4, 61 0E 00, Cmd 02, MIC: 05 5C 0A F7
# 4. Turn ON:
#    Seq F1 (or F5? Let's check next)

# Notice: Every turn operation sends TWO consecutive packets:
# Packet A: Cmd 03, Seq N
# Packet B: Cmd 02, Seq N+1

# Also notice:
# Line 59: [PACKET] [I][finder_rx:060]: YESLY [05:61:03:A3:60:E2] RSSI:-95 MF:05 00 85 07 82 00 00 00 00 
# LOOK AT THAT PACKET!
# "MF: 05 00 85 07 82 00 00 00 00" !
# 05 00 85 07 is the target actuator!
print("Captured command analysis ready.")
