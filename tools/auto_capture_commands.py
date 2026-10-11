import asyncio
import urllib.request
import json
import time
from aioesphomeapi import APIClient, LogLevel

HA_TOKEN = "YOUR_HOME_ASSISTANT_LONG_LIVED_ACCESS_TOKEN"
HA_HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

def call_ha_service(domain, service, entity_id):
    url = f"http://spiderassistant:8123/api/services/{domain}/{service}"
    data = json.dumps({"entity_id": entity_id}).encode()
    req = urllib.request.Request(url, data=data, headers=HA_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status
    except Exception as e:
        print(f"Error calling {domain}.{service}: {e}")
        return None

captured_packets = []

async def main():
    cli = APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    await cli.connect(login=True)

    def on_log(msg):
        text = msg.message.decode("utf-8", errors="ignore") if isinstance(msg.message, bytes) else str(msg.message)
        # We want command packets (len 9, typically ending with MF:.. 61 0E 00) or 85:07
        if "61 0E 00" in text or "85 07" in text:
            print(f"[PACKET] {text.strip()}")
            captured_packets.append(text.strip())

    cli.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_INFO)
    print("Listening to BLE traffic on proxy...")
    await asyncio.sleep(2)

    # 1. Turn OFF
    print("\n--- [STEP 1] Calling turn_off light.luce_tv ---")
    call_ha_service("light", "turn_off", "light.luce_tv")
    await asyncio.sleep(5)

    # 2. Turn ON
    print("\n--- [STEP 2] Calling turn_on light.luce_tv ---")
    call_ha_service("light", "turn_on", "light.luce_tv")
    await asyncio.sleep(5)

    # 3. Turn OFF
    print("\n--- [STEP 3] Calling turn_off light.luce_tv ---")
    call_ha_service("light", "turn_off", "light.luce_tv")
    await asyncio.sleep(5)

    # 4. Turn ON
    print("\n--- [STEP 4] Calling turn_on light.luce_tv ---")
    call_ha_service("light", "turn_on", "light.luce_tv")
    await asyncio.sleep(5)

    await cli.disconnect()
    print(f"\nDone! Total captured packets: {len(captured_packets)}")

if __name__ == "__main__":
    asyncio.run(main())
