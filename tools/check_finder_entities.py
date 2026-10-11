import urllib.request
import json

token = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

req = urllib.request.Request("http://spiderassistant:8123/api/states", headers=headers)
with urllib.request.urlopen(req, timeout=5) as resp:
    states = json.loads(resp.read().decode())
    finder_entities = [s for s in states if "finder" in s.get("entity_id", "") or "soggiorno" in str(s.get("attributes", {})).lower()]
    print(f"Total finder entities found: {len(finder_entities)}")
    for s in finder_entities:
        print(f" - {s.get('entity_id')}: {s.get('state')} | name={s.get('attributes', {}).get('friendly_name')}")
