import asyncio
import aioesphomeapi
import sys

async def main():
    button_name = sys.argv[1] if len(sys.argv) > 1 else "Test Finder Luce TV ON"
    cli = aioesphomeapi.APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    await cli.connect(login=True)
    entities, services = await cli.list_entities_services()
    print("Found entities:")
    target_key = None
    for e in entities:
        name = getattr(e, "name", "")
        obj_id = getattr(e, "object_id", "")
        key = getattr(e, "key", 0)
        print(f" - {name} (key: {key}, id: {obj_id}, type: {type(e).__name__})")
        if button_name.lower() in name.lower() or button_name.lower() in obj_id.lower():
            target_key = key

    if target_key:
        print(f"Triggering button key {target_key}...")
        cli.button_command(target_key)
        await asyncio.sleep(1)
        print("Triggered successfully!")
    else:
        print(f"Button '{button_name}' not found.")
    await cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
