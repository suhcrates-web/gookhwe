import requests

url = 'wss://smi.webcast.go.kr/HR'
temp = requests.post(url)
print(temp.content.decode())