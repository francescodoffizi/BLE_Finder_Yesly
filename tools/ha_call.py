import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("http://spiderassistant.local:8123/api/")
print("Testing HA URL...")
try:
    with urllib.request.urlopen("http://spiderassistant:8123/", timeout=2) as r:
        print("spiderassistant:8123 status:", r.status)
except Exception as e:
    print("Error:", e)
