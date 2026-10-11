import urllib.request
import json

token = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

req = urllib.request.Request("http://spiderassistant:8123/api/states/light.luce_tv", headers=headers)
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        print("light.luce_tv data:", json.loads(resp.read().decode()))
except Exception as e:
    print("Error:", e)
