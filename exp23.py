import websockets
import asyncio

async def listen():
    url ="wss://smi.webcast.go.kr/HR"

    async with websockets.connect(url) as ws:
        msg = await ws.recv()
        print(msg)


asyncio.get_event_loop().run_until_complete(listen())