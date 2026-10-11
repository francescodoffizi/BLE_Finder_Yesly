import urllib.request
import json
import asyncio
from aioesphomeapi import APIClient, LogLevel

HA_TOKEN = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"
HA_HEADERS = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}

def call_ha(service, entity_id):
    url = f"http://spiderassistant:8123/api/services/light/{service}"
    data = json.dumps({"entity_id": entity_id}).encode()
    req = urllib.request.Request(url, data=data, headers=HA_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status
    except Exception as e:
        print("HA err:", e)

async def main():
    cli = APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    await cli.connect(login=True)

    def on_log(msg):
        text = msg.message.decode("utf-8", errors="ignore") if isinstance(msg.message, bytes) else str(msg.message)
        if "61 0E 00" in text or "82 00 00" in text:
            print(f"[CMD PACKET] {text.strip()}")

    cli.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_INFO)
    await asyncio.sleep(1)

    print("\n--- Testing light.luce_balcone_soggiorno (different device!) ---")
    call_ha("turn_on", "light.luce_balcone_soggiorno")
    await asyncio.sleep(4)
    call_ha("turn_off", "light.luce_balcone_soggiorno")
    await asyncio.sleep(4)

    await cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
