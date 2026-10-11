import urllib.request
import json
import ssl

token = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

req = urllib.request.Request("http://spiderassistant:8123/api/states/light.luce_tv", headers=headers)
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode())
        print("Success! State of light.luce_tv:", data.get("state"))
        print("Attributes:", data.get("attributes"))
except Exception as e:
    print("API Error:", e)
