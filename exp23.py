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
# wss0 = 'wss://smiai.webcast.go.kr:8091/aistt/bokji/hls'
# wss0 = 'wss://smi.webcast.go.kr:8091/HL'
wss0 = 'wss://smi.webcast.go.kr/socket.io/?EIO=3&transport=websocket&sid=eYKEQg09sreVgH98AAIe'

async def connect():
    async with websockets.connect(wss0) as websocket:
        while True:
            message = await websocket.recv()
            print(message)

asyncio.run(connect())