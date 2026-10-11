import asyncio
import sys
from aioesphomeapi import APIClient, LogLevel

async def main():
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    client = APIClient('10.0.1.48', 6053, password=None, noise_psk='YOUR_ESPHOME_NOISE_PSK')
    await client.connect(login=True)
    print("Connected to bluetooth-proxy-sara. Listening for logs...")

    def on_log(msg):
        # Decode and print log message
        text = msg.message
        print(text)

    client.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_INFO)
    await asyncio.sleep(duration)
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
