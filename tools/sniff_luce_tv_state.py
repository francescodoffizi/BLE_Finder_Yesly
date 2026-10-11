import asyncio
import aioesphomeapi

async def main():
    cli = aioesphomeapi.APIClient("10.0.1.48", 6053, password=None, noise_psk="YOUR_ESPHOME_NOISE_PSK")
    await cli.connect(login=True)

    def on_log(msg):
        text = msg.message.decode("utf-8", errors="ignore") if isinstance(msg.message, bytes) else str(msg.message)
        if "85 07" in text:
            print(f"[STATUS] {text}")

    cli.subscribe_logs(on_log, log_level=aioesphomeapi.LogLevel.LOG_LEVEL_INFO)
    print("Listening for Luce TV telemetry for 5 seconds...")
    await asyncio.sleep(5)
    await cli.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
