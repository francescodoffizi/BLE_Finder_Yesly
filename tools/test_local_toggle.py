import asyncio
from aioesphomeapi import APIClient, LogLevel

async def main():
    cli = APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    print("Connecting to bluetooth-proxy-sara...")
    await cli.connect(login=True)
    print("Connected successfully!")

    def on_log(msg):
        text = msg.message.decode("utf-8", errors="ignore") if isinstance(msg.message, bytes) else str(msg.message)
        print(f"[ESP] {text.strip()}")

    cli.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_INFO)
    await asyncio.sleep(2)

    entities, services = await cli.list_entities_services()
    print("\n--- Available Entities on Proxy ---")
    btn_key = None
    for e in entities:
        print(f"Entity: {e.name} (key={e.key}, id={getattr(e, 'object_id', '')})")
        if "Luce TV Toggle" in e.name:
            btn_key = e.key

    if btn_key is not None:
        print(f"\n>>> Triggering Button 'Luce TV Toggle (Local BLE Direct)' (key={btn_key}) <<<")
        cli.button_command(btn_key)
    else:
        print("Button not found in entities!")

    print("Waiting 10 seconds to observe logs & telemetry...")
    await asyncio.sleep(10)

    await cli.disconnect()
    print("Disconnected.")

if __name__ == "__main__":
    asyncio.run(main())
