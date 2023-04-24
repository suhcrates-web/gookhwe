import websockets
import asyncio

# async def listen():
#     # url ="wss://smi.webcast.go.kr/33"
#     url ="wss://smiai.webcast.go.kr:8091/aistt/bokji/hls"

#     async with websockets.connect(url) as ws:
#         msg = await ws.recv()
#         print(msg)


# asyncio.get_event_loop().run_until_complete(listen())

import asyncio
import websockets

async def connect():
    async with websockets.connect('wss://smiai.webcast.go.kr:8091/aistt/bokji/hls') as websocket:
        while True:
            message = await websocket.recv()
            print(message)

asyncio.run(connect())