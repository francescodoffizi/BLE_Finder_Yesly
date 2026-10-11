import base64
b64 = "agRdAngNZbysHAUvCyQKlg=="
raw = base64.b64decode(b64)
print("Gateway sub 5 (b64):", b64)
print("Gateway sub 5 (hex):", raw.hex(), "len:", len(raw))
