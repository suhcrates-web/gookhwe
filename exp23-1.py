import asyncio
import websockets

wss2 = 'wss://smi.webcast.go.kr/socket.io/?EIO=3&transport=websocket&sid=eYKEQg09sreVgH98AAIe'

async def connect():
    while True:
        try:
            async with websockets.connect(wss2) as websocket:
                while True:
                    message = await websocket.recv()
                    print(message)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed: {e}")
            # Wait for a few seconds before trying to reconnect
            await asyncio.sleep(5)
            continue

asyncio.run(connect())