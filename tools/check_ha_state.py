import urllib.request
import json

token = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

req = urllib.request.Request("http://spiderassistant:8123/api/states/light.luce_tv", headers=headers)
with urllib.request.urlopen(req, timeout=5) as resp:
    data = json.loads(resp.read().decode())
    print("Current State of light.luce_tv:", data.get("state"))
