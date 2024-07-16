##### 이거다 이거 #######

import requests
import json
import re
import websockets
import asyncio
import time



async def do():
    header1 = {'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
'Connection': 'keep-alive',
'Content-Length': '8',
'Content-type': 'text/plain;charset=UTF-8',
'Cookie': '_ga=GA1.1.384811004.1688001248; _ga_QEPEGVC0VX=GS1.1.1688016651.3.1.1688017420.0.0.0; io=GWJO9aL2mZjFOMpxAAHt',
'Host': 'smi.webcast.go.kr',
'Origin': 'https://assembly.webcast.go.kr',
'Referer': 'https://assembly.webcast.go.kr/',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-site',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"'}

    url = 'https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling'

    temp = requests.get(url)
    text0 = temp.content.decode('utf-8')
    text0 = re.search(r'\{.*\}', text0)[0]
    text0 = json.loads(text0)
    sid = text0['sid']
    print(sid)
    wss2 = 'https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling&t=Oa5hntB&sid=' + sid
    # temp0 = requests.post(wss2)
    # print(temp0.content)
    header2 = {'Host': 'smi.webcast.go.kr',
               'Connection': 'Upgrade',
               'Pragma': 'no-cache',
               'Cache-Control': 'no-cache',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
               'Upgrade': 'websocket',
               'Origin': 'https://assembly.webcast.go.kr',
               'Sec-WebSocket-Version': '13',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
               'Sec-WebSocket-Key':
                   'f6ICdxQdSqGf0aUeR3g0+g==',
               'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits'}
    wss0 = 'wss://smi.webcast.go.kr/socket.io/?EIO=3&transport=websocket&t=Oa5hnt&sid=' + sid
    async with websockets.connect(wss0) as websocket:

        # while True:
        await websocket.send("2probe")
        message = await websocket.recv()
        print('here')
        print(message)
        # message = json.loads(message)
        time.sleep(2)
        await websocket.send("5")     # 이렇게 주거니 받거니 해야 그다음에 오는듯

        message = await websocket.recv()
        print(message)
        await websocket.send("2")  # 이렇게 주거니 받거니 해야 그다음에 오는듯
        message = await websocket.recv()
        print(message)
        # print(message['final'])
        # print(message['transcript'])
        # print(message['transcripts'][0][0])
        # print(message['transcripts'][0][-1])
        print("================")
        await websocket.close(1000, "Normal closure")
asyncio.run(do())
# asyncio.get_event_loop().run_until_complete(do())