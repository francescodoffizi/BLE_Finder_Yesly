import asyncio
import urllib.request
import json
from aioesphomeapi import APIClient, LogLevel

HA_TOKEN = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"

def call_ha(service):
    url = f"http://spiderassistant:8123/api/services/light/{service}"
    data = json.dumps({"entity_id": "light.luce_tv"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return resp.status

async def main():
    cli = APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    await cli.connect(login=True)

    def on_log(msg):
        text = msg.message.decode("utf-8", errors="ignore") if isinstance(msg.message, bytes) else str(msg.message)
        if "85:07" in text or "85 07" in text or "61 0E" in text or "A3:60:E2" in text or "finder_tx" in text or "finder_cmd" in text:
            print(f"[LOG] {text.strip()}")

    cli.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_INFO)
    await asyncio.sleep(2)

    print("\n--- Triggering HA turn_off light.luce_tv ---")
    call_ha("turn_off")
    await asyncio.sleep(4)

    print("\n--- Triggering HA turn_on light.luce_tv ---")
    call_ha("turn_on")
    await asyncio.sleep(4)

    await cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
