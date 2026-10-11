import asyncio
import sys
from aioesphomeapi import APIClient

async def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "list"
    client = APIClient('10.0.1.48', 6053, password=None, noise_psk='YOUR_ESPHOME_NOISE_PSK')
    await client.connect(login=True)

    entities, services = await client.list_entities_services()
    buttons = [e for e in entities if "button" in type(e).__name__.lower()]
    
    if action == "list":
        print("Available Buttons on bluetooth-proxy-sara:")
        for b in buttons:
            print(f"  - Key: {b.key} | Name: {b.name} | Object ID: {b.object_id}")
    else:
        target = next((b for b in buttons if action.lower() in b.name.lower() or action.lower() in b.object_id.lower()), None)
        if target:
            print(f"Pressing button: {target.name} (Key: {target.key})...")
            await client.button_command(target.key)
            print("Button press command sent successfully!")
        else:
            print(f"Button '{action}' not found among: {[b.name for b in buttons]}")

    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
