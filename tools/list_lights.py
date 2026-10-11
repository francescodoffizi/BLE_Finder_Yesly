import urllib.request
import json

token = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

req = urllib.request.Request("http://spiderassistant:8123/api/states", headers=headers)
with urllib.request.urlopen(req, timeout=5) as resp:
    states = json.loads(resp.read().decode())
    for s in states:
        eid = s.get("entity_id", "")
        if "luce" in eid or "tv" in eid or "light" in eid:
            print(f"{eid}: {s.get('state')} ({s.get('attributes', {}).get('friendly_name')})")
