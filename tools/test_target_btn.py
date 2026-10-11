import asyncio
import aioesphomeapi

async def main():
    cli = aioesphomeapi.APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    await cli.connect(login=True)

    def on_log(msg):
        text = msg.message.decode("utf-8", errors="ignore") if isinstance(msg.message, bytes) else str(msg.message)
        if any(k in text for k in ["85 07", "finder_cmd", "finder_tx"]):
            print(f"[TEST LOG] {text}")

    cli.subscribe_logs(on_log, log_level=aioesphomeapi.LogLevel.LOG_LEVEL_INFO)

    entities, services = await cli.list_entities_services()
    btn = next((e for e in entities if "Direct Target" in getattr(e, "name", "")), None)
    if btn:
        print(f"Triggering button: {btn.name} (key: {btn.key})...")
        cli.button_command(btn.key)

    await asyncio.sleep(6)
    await cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
