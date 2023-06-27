# import requests
# import json
# url = "https://assembly.webcast.go.kr/main/service/live_list.asp"
# response = requests.get(url)
# print(json.loads(response.content))
import websockets
import json
import re
a = '//thumb.webcast.go.kr/api/thumbnail/bokji'
wss0 =f'wss://smiai.webcast.go.kr:8091/aistt/bokji/hls'
b = re.search(r'(?<=/)[^/]+$',a)
# b = re.search(r'/(\w+)$',a)
print(b[0])

async def connect(wss0):
    async with websockets.connect(wss0) as websocket:
        while True:
            message = await websocket.recv()
            message = json.loads(message)
            print(message)
connect(wss0)