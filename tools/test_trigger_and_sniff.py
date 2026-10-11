import asyncio
import aioesphomeapi

async def main():
    cli = aioesphomeapi.APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    await cli.connect(login=True)

    def on_log(msg):
        text = msg.message
        if isinstance(text, bytes):
            text = text.decode("utf-8", errors="ignore")
        if "85 07" in text or "finder_cmd" in text or "finder_tx" in text:
            print(f"[LIVE LOG] {text}")

    cli.subscribe_logs(on_log, log_level=aioesphomeapi.LogLevel.LOG_LEVEL_INFO)

    entities, services = await cli.list_entities_services()
    buttons = {e.name: e.key for e in entities if "Button" in type(e).__name__}
    print("Available buttons:", buttons)

    target_on = buttons.get("Test Finder Luce TV ON")
    if target_on:
        print(f"--> Triggering 'Test Finder Luce TV ON' (key: {target_on})...")
        cli.button_command(target_on)

    # Listen for 6 seconds to observe mesh responses
    await asyncio.sleep(6)
    await cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
