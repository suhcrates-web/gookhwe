import requests
import re
import json


url = 'https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling'

temp = requests.get(url)
text0 = temp.content.decode('utf-8')
text0 = re.search(r'\{.*\}', text0)[0]
text0 = json.loads(text0)
sid = text0['sid']
print(sid)

print(temp.cookies.get('_ga'))
wss2 = 'https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling&t=Oa5hntB&sid=' + sid

header1 = {'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
'Connection': 'keep-alive',
'Content-Length': '8',
'Content-type': 'text/plain;charset=UTF-8',
'Cookie': f'_ga=GA1.1.384811004.1688001248; _ga_QEPEGVC0VX=GS1.1.1688016651.3.1.1688017420.0.0.0; io={sid}',
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

temp0 = requests.post(wss2, headers=header1)
print(temp0.content)