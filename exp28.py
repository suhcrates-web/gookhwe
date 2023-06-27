import websockets
import asyncio
import json
wss0 = 'wss://smiai.webcast.go.kr:8091/aistt/gyoyuk/hls'
async def do(wss0):
    async with websockets.connect(wss0) as websocket:
        while True:
            message = await websocket.recv()
            message = json.loads(message)
            print(message['final'])
            print(message['transcript'])
            print(message['transcripts'][0][0])
            print(message['transcripts'][0][-1])
            print("================")
asyncio.run(do(wss0))