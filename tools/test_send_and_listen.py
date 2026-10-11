import asyncio
import sys
from aioesphomeapi import APIClient, LogLevel

async def main():
    button_name = sys.argv[1] if len(sys.argv) > 1 else "Test Finder Luce Cameretta ON"
    client = APIClient('10.0.1.48', 6053, password=None, noise_psk='YOUR_ESPHOME_NOISE_PSK')
    await client.connect(login=True)

    def on_log(msg):
        print(f"[ESP32 LOG] {msg.message}")

    client.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_INFO)

    entities, services = await client.list_entities_services()
    buttons = [e for e in entities if "button" in type(e).__name__.lower()]
    target = next((b for b in buttons if button_name.lower() in b.name.lower()), None)
    
    if not target:
        print(f"Button '{button_name}' not found.")
        await client.disconnect()
        return

    await asyncio.sleep(1)
    client.button_command(target.key)

    await asyncio.sleep(5)
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
