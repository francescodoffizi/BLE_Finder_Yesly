# Opcode sequence:
# 02: ldarg.0 (buttonIndex)
# 16: ldc.i4.0
# 2f 03: bge.s +3 (if buttonIndex >= 0 goto label1)
# 16: ldc.i4.0
# 2b 0c: br.s +12 (goto label2)
# label1:
# 03: ldarg.1 (isPressed)
# 16: ldc.i4.0
# fe 03: ceq (isPressed == 0)
# 17: ldc.i4.1 (1)
# 02: ldarg.0 (buttonIndex)
# 1f 1f: ldc.i4.s 0x1F (31)
# 5f: and (0x5E is and, 0x5F is or) -> wait, let's verify if 0x5E is and or 0x5F
# 62: shr (wait, 61 is shl, 62 is shr)
# 60: xor
# d2: conv.u1
# 0a: stloc.0
# 14: ldnull
# 06: ldloc.0
# 14: ldnull
# call CreateInputBufferForAdv(null, loc.0, null, 4)

def calc_button_byte(buttonIndex, isPressed):
    if buttonIndex < 0:
        return 0
    # in CLR:
    # 03: isPressed
    # 16: 0
    # fe 03: ceq -> 1 if not isPressed else 0
    # 17: 1
    # 02: buttonIndex
    # 1f 1f: 31
    # 5e/5f: & 31
    # 61/62: << (buttonIndex & 31)
    # 60: ^
    v_ceq = 1 if not isPressed else 0
    # Let's test combinations of (1 << (buttonIndex & 31)) ^ v_ceq
    val1 = (1 << (buttonIndex & 31)) ^ v_ceq
    val2 = (v_ceq << (buttonIndex & 31)) ^ 1
    return val1 & 0xFF, val2 & 0xFF

for b in [0, 1]:
    for p in [True, False]:
        print(f"buttonIndex={b}, isPressed={p} -> {calc_button_byte(b, p)}")
